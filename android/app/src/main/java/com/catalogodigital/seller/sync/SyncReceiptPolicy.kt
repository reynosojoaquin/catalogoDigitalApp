package com.catalogodigital.seller.sync

import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.data.local.PendingOperation

object SyncReceiptPolicy {
    private val terminalStatuses = setOf(
        OperationStatus.APPLIED,
        OperationStatus.CONFLICT,
        OperationStatus.REJECTED,
    )

    fun requireValid(operations: List<PendingOperation>, results: List<OperationResult>) {
        val expectedIds = operations.map(PendingOperation::operationId).toSet()
        require(expectedIds.size == operations.size) { "Claimed operation IDs must be unique." }
        require(results.size == operations.size) { "The server must return one result per operation." }
        require(results.map(OperationResult::operationId).toSet() == expectedIds) {
            "Synchronization results do not match the submitted operations."
        }
        require(results.map(OperationResult::operationId).distinct().size == results.size) {
            "Synchronization results cannot repeat an operation."
        }
        val byId = operations.associateBy(PendingOperation::operationId)
        results.forEach { result ->
            val operation = requireNotNull(byId[result.operationId])
            require(result.status in terminalStatuses) { "The synchronization status is not terminal." }
            require(result.entityType == operation.operationType.removeSuffix("_create")) {
                "The synchronization entity type is inconsistent."
            }
            require(result.status != OperationStatus.APPLIED || result.entityId != null) {
                "An applied operation requires a server entity ID."
            }
            require(operation.entityId == null || result.entityId == null || operation.entityId == result.entityId) {
                "The synchronization entity ID is inconsistent."
            }
        }
    }
}
