package com.catalogodigital.seller.sync

import com.catalogodigital.seller.data.local.PendingOperation

object SyncBatchPolicy {
    const val MAX_OPERATIONS = 50

    fun requireValid(operations: List<PendingOperation>) {
        require(operations.isNotEmpty()) { "A synchronization batch cannot be empty." }
        require(operations.size <= MAX_OPERATIONS) { "A synchronization batch cannot exceed $MAX_OPERATIONS operations." }
        require(operations.map(PendingOperation::deviceId).distinct().size == 1) {
            "All synchronization operations must belong to the same device."
        }
    }
}
