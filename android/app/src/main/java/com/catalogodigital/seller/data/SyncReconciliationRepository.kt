package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.PendingOperation
import com.catalogodigital.seller.sync.OperationResult
import com.catalogodigital.seller.sync.SyncReceiptPolicy

class SyncReconciliationRepository(private val database: CatalogDatabase) {
    suspend fun apply(operations: List<PendingOperation>, results: List<OperationResult>) {
        SyncReceiptPolicy.requireValid(operations, results)
        val operationsById = operations.associateBy(PendingOperation::operationId)
        database.withTransaction {
            results.forEach { result ->
                val operation = requireNotNull(operationsById[result.operationId])
                database.pendingOperationDao().updateResult(
                    result.operationId,
                    result.status,
                    result.conflictCode,
                )
                val entityId = result.entityId ?: operation.entityId
                if (entityId != null) {
                    when (operation.operationType) {
                        "customer_create" -> database.customerDraftDao().updateStatus(entityId, result.status)
                        "order_create" -> database.orderDraftDao().updateStatus(entityId, result.status)
                        "payment_create" -> database.paymentDraftDao().updateStatus(entityId, result.status)
                    }
                }
            }
        }
    }
}
