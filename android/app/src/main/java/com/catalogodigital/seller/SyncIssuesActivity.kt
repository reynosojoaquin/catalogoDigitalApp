package com.catalogodigital.seller

import android.os.Bundle
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.data.local.PendingOperation
import com.catalogodigital.seller.databinding.ActivitySyncIssuesBinding
import com.catalogodigital.seller.sync.SyncIssuePolicy
import com.catalogodigital.seller.sync.SyncIssueReason
import kotlinx.coroutines.launch

class SyncIssuesActivity : ComponentActivity() {
    private lateinit var binding: ActivitySyncIssuesBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySyncIssuesBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val dao = (application as CatalogApplication).database.pendingOperationDao()
        lifecycleScope.launch {
            dao.observeIssues(listOf(OperationStatus.CONFLICT, OperationStatus.REJECTED)).collect(::render)
        }
    }

    private fun render(operations: List<PendingOperation>) {
        binding.issueList.removeAllViews()
        if (operations.isEmpty()) {
            binding.issueList.addView(textView(getString(R.string.sync_issues_empty)))
            return
        }
        operations.forEach { operation ->
            binding.issueList.addView(
                textView(
                    getString(
                        R.string.sync_issue_format,
                        operationLabel(operation.operationType),
                        statusLabel(operation.status),
                        reasonLabel(operation.conflictCode),
                        operation.clientTimestamp,
                    ),
                ),
            )
        }
    }

    private fun textView(value: String) = TextView(this).apply {
        text = value
        setPadding(0, 16, 0, 16)
    }

    private fun operationLabel(type: String): String = getString(
        when (type) {
            "customer_create" -> R.string.sync_operation_customer
            "order_create" -> R.string.sync_operation_order
            "payment_create" -> R.string.sync_operation_payment
            "return_create" -> R.string.sync_operation_return
            else -> R.string.sync_operation_unknown
        },
    )

    private fun statusLabel(status: String): String = getString(
        if (status == OperationStatus.CONFLICT) R.string.sync_status_conflict
        else R.string.sync_status_rejected,
    )

    private fun reasonLabel(code: String?): String = getString(
        when (SyncIssuePolicy.reason(code)) {
            SyncIssueReason.DUPLICATE_CUSTOMER -> R.string.sync_reason_duplicate_customer
            SyncIssueReason.INVALID_REFERENCE -> R.string.sync_reason_invalid_reference
            SyncIssueReason.IDEMPOTENCY_CONFLICT -> R.string.sync_reason_idempotency_conflict
            SyncIssueReason.INVOICE_NOT_PAYABLE -> R.string.sync_reason_invoice_not_payable
            SyncIssueReason.RETURN_CONFLICT -> R.string.sync_reason_return_conflict
            SyncIssueReason.INVALID_PAYLOAD -> R.string.sync_reason_invalid_payload
            SyncIssueReason.BATCH_REJECTED -> R.string.sync_reason_batch_rejected
            SyncIssueReason.UNKNOWN -> R.string.sync_reason_unknown
        },
    )
}
