package com.catalogodigital.seller

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.local.BusinessDocumentEntity
import com.catalogodigital.seller.databinding.ActivityBusinessDocumentsBinding
import kotlinx.coroutines.launch
import java.math.BigDecimal
import java.text.NumberFormat

class BusinessDocumentsActivity : ComponentActivity() {
    private lateinit var binding: ActivityBusinessDocumentsBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityBusinessDocumentsBinding.inflate(layoutInflater)
        setContentView(binding.root)
        val dao = (application as CatalogApplication).database.businessDocumentDao()
        lifecycleScope.launch {
            dao.observeAll().collect { documents ->
                binding.documents.text = if (documents.isEmpty()) {
                    getString(R.string.business_documents_empty)
                } else {
                    documents.joinToString("\n\n", transform = ::formatDocument)
                }
            }
        }
    }

    private fun formatDocument(document: BusinessDocumentEntity): String = getString(
        R.string.business_document_format,
        getString(typeResource(document.entityType)),
        getString(statusResource(document.entityType, document.status)),
        formatMoney(document.amountMinor ?: 0),
    )

    private fun typeResource(type: String): Int = when (type) {
        "order" -> R.string.business_type_order
        "invoice" -> R.string.business_type_invoice
        "payment" -> R.string.business_type_payment
        "return" -> R.string.business_type_return
        "commission" -> R.string.business_type_commission
        "settlement" -> R.string.business_type_settlement
        else -> R.string.status_unknown
    }

    private fun statusResource(type: String, status: String?): Int = when (status) {
        "submitted" -> R.string.status_submitted
        "delivered" -> R.string.status_delivered
        "cancelled" -> R.string.status_cancelled
        "unpaid" -> R.string.status_unpaid
        "paid" -> R.string.status_paid
        "reported" -> R.string.status_reported
        "confirmed" -> R.string.status_confirmed
        "available" -> R.string.status_available
        "settled" -> R.string.status_settled
        null -> if (type == "settlement") R.string.status_confirmed else R.string.status_unknown
        else -> R.string.status_unknown
    }

    private fun formatMoney(minor: Long): String = NumberFormat.getCurrencyInstance().format(
        BigDecimal.valueOf(minor).movePointLeft(2),
    )
}
