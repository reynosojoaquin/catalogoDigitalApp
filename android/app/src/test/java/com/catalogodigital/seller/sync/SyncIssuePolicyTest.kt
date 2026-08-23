package com.catalogodigital.seller.sync

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SyncIssuePolicyTest {
    @Test
    fun mapsEveryServerConflictCodeToAVisibleReason() {
        val expected = mapOf(
            "duplicate_customer" to SyncIssueReason.DUPLICATE_CUSTOMER,
            "invalid_order_reference" to SyncIssueReason.INVALID_REFERENCE,
            "idempotency_mismatch" to SyncIssueReason.IDEMPOTENCY_CONFLICT,
            "order_idempotency_conflict" to SyncIssueReason.IDEMPOTENCY_CONFLICT,
            "payment_idempotency_conflict" to SyncIssueReason.IDEMPOTENCY_CONFLICT,
            "invoice_not_payable" to SyncIssueReason.INVOICE_NOT_PAYABLE,
            "return_conflict" to SyncIssueReason.RETURN_CONFLICT,
            "invalid_payload" to SyncIssueReason.INVALID_PAYLOAD,
            "batch_rejected" to SyncIssueReason.BATCH_REJECTED,
        )

        expected.forEach { (code, reason) -> assertEquals(reason, SyncIssuePolicy.reason(code)) }
    }

    @Test
    fun unknownOrMissingCodeDoesNotExposeInternalValue() {
        assertEquals(SyncIssueReason.UNKNOWN, SyncIssuePolicy.reason("future_code"))
        assertEquals(SyncIssueReason.UNKNOWN, SyncIssuePolicy.reason(null))
    }

    @Test
    fun classifiesAuthenticationPermanentAndTransientFailures() {
        assertEquals(SyncFailureAction.AUTHENTICATION_REQUIRED, SyncFailurePolicy.action(401))
        assertEquals(SyncFailureAction.AUTHENTICATION_REQUIRED, SyncFailurePolicy.action(403))
        assertEquals(SyncFailureAction.REJECT_BATCH, SyncFailurePolicy.action(400))
        assertEquals(SyncFailureAction.RETRY, SyncFailurePolicy.action(408))
        assertEquals(SyncFailureAction.RETRY, SyncFailurePolicy.action(429))
        assertEquals(SyncFailureAction.RETRY, SyncFailurePolicy.action(503))
    }

    @Test
    fun reconciledBatchIsNotResetWhenAFeedFailsAfterPush() {
        assertTrue(SyncBatchRecoveryPolicy.shouldResetClaimedOperations(false))
        assertFalse(SyncBatchRecoveryPolicy.shouldResetClaimedOperations(true))
    }
}
