package com.catalogodigital.seller.sync

import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.data.local.PendingOperation
import org.junit.Assert.assertThrows
import org.junit.Test
import java.time.Instant
import java.util.UUID

class SyncReceiptPolicyTest {
    @Test
    fun acceptsOneMatchingTerminalResultPerOperation() {
        val operation = operation()
        SyncReceiptPolicy.requireValid(
            listOf(operation),
            listOf(result(operation, OperationStatus.APPLIED, operation.entityId)),
        )
    }

    @Test
    fun rejectsMissingResult() {
        assertThrows(IllegalArgumentException::class.java) {
            SyncReceiptPolicy.requireValid(listOf(operation()), emptyList())
        }
    }

    @Test
    fun rejectsRepeatedResult() {
        val operation = operation()
        val result = result(operation, OperationStatus.CONFLICT, null)
        assertThrows(IllegalArgumentException::class.java) {
            SyncReceiptPolicy.requireValid(listOf(operation()), listOf(result, result))
        }
    }

    @Test
    fun rejectsNonTerminalStatus() {
        val operation = operation()
        assertThrows(IllegalArgumentException::class.java) {
            SyncReceiptPolicy.requireValid(
                listOf(operation),
                listOf(result(operation, OperationStatus.IN_FLIGHT, null)),
            )
        }
    }

    @Test
    fun rejectsMismatchedEntityId() {
        val operation = operation()
        assertThrows(IllegalArgumentException::class.java) {
            SyncReceiptPolicy.requireValid(
                listOf(operation),
                listOf(result(operation, OperationStatus.APPLIED, UUID.randomUUID().toString())),
            )
        }
    }

    private fun operation(): PendingOperation = PendingOperation(
        operationId = UUID.randomUUID().toString(),
        operationType = "order_create",
        entityId = UUID.randomUUID().toString(),
        idempotencyKey = UUID.randomUUID().toString(),
        deviceId = UUID.randomUUID().toString(),
        clientTimestamp = Instant.EPOCH.toString(),
        clientVersion = 1,
        encryptedPayload = byteArrayOf(),
        payloadIv = byteArrayOf(),
    )

    private fun result(operation: PendingOperation, status: String, entityId: String?) = OperationResult(
        operationId = operation.operationId,
        entityType = "order",
        entityId = entityId,
        status = status,
        conflictCode = null,
    )
}
