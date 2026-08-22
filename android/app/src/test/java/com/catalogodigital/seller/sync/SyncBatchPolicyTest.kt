package com.catalogodigital.seller.sync

import com.catalogodigital.seller.data.local.PendingOperation
import org.junit.Assert.assertThrows
import org.junit.Test
import java.time.Instant
import java.util.UUID

class SyncBatchPolicyTest {
    @Test
    fun acceptsOperationsFromOneDevice() {
        val deviceId = UUID.randomUUID().toString()
        SyncBatchPolicy.requireValid(listOf(operation(deviceId), operation(deviceId)))
    }

    @Test
    fun rejectsMixedDevices() {
        assertThrows(IllegalArgumentException::class.java) {
            SyncBatchPolicy.requireValid(
                listOf(operation(UUID.randomUUID().toString()), operation(UUID.randomUUID().toString())),
            )
        }
    }

    @Test
    fun rejectsEmptyBatch() {
        assertThrows(IllegalArgumentException::class.java) {
            SyncBatchPolicy.requireValid(emptyList())
        }
    }

    @Test
    fun rejectsOversizedBatch() {
        assertThrows(IllegalArgumentException::class.java) {
            val deviceId = UUID.randomUUID().toString()
            SyncBatchPolicy.requireValid(List(SyncBatchPolicy.MAX_OPERATIONS + 1) { operation(deviceId) })
        }
    }

    private fun operation(deviceId: String) = PendingOperation(
        operationId = UUID.randomUUID().toString(),
        operationType = "customer_create",
        idempotencyKey = UUID.randomUUID().toString(),
        deviceId = deviceId,
        clientTimestamp = Instant.EPOCH.toString(),
        clientVersion = 1,
        encryptedPayload = byteArrayOf(),
        payloadIv = byteArrayOf(),
    )
}
