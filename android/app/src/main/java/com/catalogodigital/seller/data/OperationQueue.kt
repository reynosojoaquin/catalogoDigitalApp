package com.catalogodigital.seller.data

import com.catalogodigital.seller.data.local.PendingOperation
import com.catalogodigital.seller.data.local.PendingOperationDao
import com.catalogodigital.seller.security.KeystoreCipher
import java.time.Instant
import java.util.UUID

class OperationQueue(
    private val dao: PendingOperationDao,
    private val cipher: KeystoreCipher = KeystoreCipher(),
) {
    suspend fun enqueue(operationType: String, entityId: UUID, deviceId: UUID, payloadJson: String) {
        dao.insert(build(operationType, entityId, deviceId, payloadJson))
    }

    fun build(operationType: String, entityId: UUID, deviceId: UUID, payloadJson: String): PendingOperation {
        val encrypted = cipher.encrypt(payloadJson.encodeToByteArray())
        return PendingOperation(
            operationId = UUID.randomUUID().toString(),
            operationType = operationType,
            entityId = entityId.toString(),
            idempotencyKey = UUID.randomUUID().toString(),
            deviceId = deviceId.toString(),
            clientTimestamp = Instant.now().toString(),
            clientVersion = 1,
            encryptedPayload = encrypted.ciphertext,
            payloadIv = encrypted.iv,
        )
    }

    fun decryptPayload(operation: PendingOperation): String = cipher.decrypt(
        com.catalogodigital.seller.security.EncryptedValue(operation.encryptedPayload, operation.payloadIv),
    ).decodeToString()
}
