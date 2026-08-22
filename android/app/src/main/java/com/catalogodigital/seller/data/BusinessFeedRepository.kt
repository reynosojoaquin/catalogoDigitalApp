package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.BusinessDocumentEntity
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.SyncCursor
import com.catalogodigital.seller.security.KeystoreCipher
import com.catalogodigital.seller.sync.BusinessFeedPage
import com.catalogodigital.seller.sync.BusinessFeedPolicy
import com.catalogodigital.seller.sync.MoneyParser
import org.json.JSONObject

class BusinessFeedRepository(
    private val database: CatalogDatabase,
    private val cipher: KeystoreCipher = KeystoreCipher(),
) {
    suspend fun cursor(): Long = database.syncCursorDao().sequence(FEED) ?: 0

    suspend fun apply(page: BusinessFeedPage) = database.withTransaction {
        val currentCursor = cursor()
        BusinessFeedPolicy.requireValid(currentCursor, page)
        page.changes.forEach { change ->
            val dao = database.businessDocumentDao()
            if ((dao.version(change.entityType, change.entityId) ?: 0) <= change.version) {
                val data = JSONObject(change.dataJson)
                val encrypted = cipher.encrypt(change.dataJson.encodeToByteArray())
                val status = data.optString("status").ifBlank { null }
                val amountField = when (change.entityType) {
                    "payment", "commission" -> "amount"
                    else -> "total"
                }
                val amount = if (data.has(amountField) && !data.isNull(amountField)) {
                    MoneyParser.toMinorUnits(data.getString(amountField))
                } else null
                val parentField = when (change.entityType) {
                    "order" -> "customer_id"
                    "invoice" -> "order_id"
                    "payment", "return", "commission" -> "invoice_id"
                    else -> null
                }
                val parentId = parentField?.let { field ->
                    if (data.has(field) && !data.isNull(field)) data.getString(field) else null
                }
                dao.upsert(BusinessDocumentEntity(
                    documentKey = "${change.entityType}:${change.entityId}",
                    entityType = change.entityType,
                    entityId = change.entityId,
                    parentId = parentId,
                    displayLabel = if (change.entityType == "invoice") {
                        data.optString("customer_name").ifBlank { null }
                    } else null,
                    version = change.version,
                    status = status,
                    amountMinor = amount,
                    occurredAt = change.occurredAt,
                    encryptedData = encrypted.ciphertext,
                    dataIv = encrypted.iv,
                ))
                if (change.entityType == "order" && status != null) {
                    database.orderDraftDao().updateStatus(change.entityId, status)
                }
                if (change.entityType == "payment" && status != null) {
                    database.paymentDraftDao().updateStatus(change.entityId, status)
                }
            }
        }
        database.syncCursorDao().upsert(SyncCursor(FEED, page.nextCursor))
    }

    private companion object {
        const val FEED = "business"
    }
}
