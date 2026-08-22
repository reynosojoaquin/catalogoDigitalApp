package com.catalogodigital.seller.data

import android.database.sqlite.SQLiteConstraintException
import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.CustomerDraftEntity
import com.catalogodigital.seller.security.LocalIdentityFingerprint
import org.json.JSONObject
import java.time.Instant
import java.util.UUID

class OfflineCustomerRepository(
    private val database: CatalogDatabase,
    private val fingerprint: LocalIdentityFingerprint = LocalIdentityFingerprint(),
) {
    suspend fun create(
        deviceId: UUID,
        fullName: String,
        email: String?,
        phone: String?,
        identity: String?,
    ): UUID {
        val input = CustomerInputNormalizer.normalize(fullName, email, phone, identity)
        val identityFingerprint = input.identity?.let(fingerprint::create)
        val customerId = UUID.randomUUID()
        val payload = JSONObject()
            .put("id", customerId.toString())
            .put("full_name", input.fullName)
            .put("email", input.email ?: JSONObject.NULL)
            .put("phone", input.phone ?: JSONObject.NULL)
            .put("identity_document", input.identity ?: JSONObject.NULL)
        val queue = OperationQueue(database.pendingOperationDao())
        val operation = queue.build("customer_create", customerId, deviceId, payload.toString())

        try {
            database.withTransaction {
                ensureUnique(input, identityFingerprint)
                database.customerDraftDao().insert(
                    CustomerDraftEntity(
                        id = customerId.toString(),
                        fullName = input.fullName,
                        email = input.email,
                        phone = input.phone,
                        identityFingerprint = identityFingerprint,
                        createdAt = Instant.now().toString(),
                    ),
                )
                database.pendingOperationDao().insert(operation)
            }
        } catch (error: SQLiteConstraintException) {
            throw DuplicateLocalCustomerException().also { it.initCause(error) }
        }
        return customerId
    }

    private suspend fun ensureUnique(input: NormalizedCustomerInput, identityFingerprint: ByteArray?) {
        val catalog = database.catalogDao()
        val drafts = database.customerDraftDao()
        val duplicate = (input.email != null && (
            catalog.countCustomersByEmail(input.email) > 0 || drafts.countByEmail(input.email) > 0
        )) || (input.phone != null && (
            catalog.countCustomersByPhone(input.phone) > 0 || drafts.countByPhone(input.phone) > 0
        )) || (identityFingerprint != null && drafts.countByIdentity(identityFingerprint) > 0)
        if (duplicate) throw DuplicateLocalCustomerException()
    }
}

class DuplicateLocalCustomerException : Exception("A matching customer already exists locally.")
