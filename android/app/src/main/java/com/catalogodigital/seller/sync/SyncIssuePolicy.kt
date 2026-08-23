package com.catalogodigital.seller.sync

enum class SyncIssueReason {
    DUPLICATE_CUSTOMER,
    INVALID_REFERENCE,
    IDEMPOTENCY_CONFLICT,
    INVOICE_NOT_PAYABLE,
    RETURN_CONFLICT,
    INVALID_PAYLOAD,
    BATCH_REJECTED,
    UNKNOWN,
}

object SyncIssuePolicy {
    fun reason(conflictCode: String?): SyncIssueReason = when (conflictCode) {
        "duplicate_customer" -> SyncIssueReason.DUPLICATE_CUSTOMER
        "invalid_order_reference" -> SyncIssueReason.INVALID_REFERENCE
        "idempotency_mismatch", "order_idempotency_conflict", "payment_idempotency_conflict" ->
            SyncIssueReason.IDEMPOTENCY_CONFLICT
        "invoice_not_payable" -> SyncIssueReason.INVOICE_NOT_PAYABLE
        "return_conflict" -> SyncIssueReason.RETURN_CONFLICT
        "invalid_payload" -> SyncIssueReason.INVALID_PAYLOAD
        "batch_rejected" -> SyncIssueReason.BATCH_REJECTED
        else -> SyncIssueReason.UNKNOWN
    }
}

enum class SyncFailureAction { AUTHENTICATION_REQUIRED, REJECT_BATCH, RETRY }

object SyncFailurePolicy {
    fun action(statusCode: Int): SyncFailureAction = when {
        statusCode == 401 || statusCode == 403 -> SyncFailureAction.AUTHENTICATION_REQUIRED
        statusCode in 400..499 && statusCode != 408 && statusCode != 429 -> SyncFailureAction.REJECT_BATCH
        else -> SyncFailureAction.RETRY
    }
}

object SyncBatchRecoveryPolicy {
    fun shouldResetClaimedOperations(reconciled: Boolean): Boolean = !reconciled
}
