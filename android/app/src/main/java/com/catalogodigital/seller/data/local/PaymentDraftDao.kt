package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

data class PayableInvoice(
    val id: String,
    val label: String?,
    val amountMinor: Long,
)

@Dao
interface PaymentDraftDao {
    @Insert
    suspend fun insert(draft: PaymentDraftEntity)

    @Query("UPDATE payment_drafts SET status = :status WHERE id = :id")
    suspend fun updateStatus(id: String, status: String)

    @Query("""
        SELECT invoice.entityId AS id, invoice.displayLabel AS label, invoice.amountMinor AS amountMinor
        FROM business_documents AS invoice
        WHERE invoice.entityType = 'invoice' AND invoice.status = 'unpaid' AND invoice.amountMinor IS NOT NULL
          AND NOT EXISTS (
            SELECT 1 FROM payment_drafts AS draft
            WHERE draft.invoiceId = invoice.entityId AND draft.status NOT IN ('conflict', 'rejected')
          )
          AND NOT EXISTS (
            SELECT 1 FROM business_documents AS payment
            WHERE payment.entityType = 'payment' AND payment.parentId = invoice.entityId
          )
        ORDER BY invoice.occurredAt, invoice.entityId
    """)
    suspend fun payableInvoices(): List<PayableInvoice>

    @Query("""
        SELECT invoice.entityId AS id, invoice.displayLabel AS label, invoice.amountMinor AS amountMinor
        FROM business_documents AS invoice
        WHERE invoice.entityType = 'invoice' AND invoice.entityId = :invoiceId
          AND invoice.status = 'unpaid' AND invoice.amountMinor IS NOT NULL
          AND NOT EXISTS (
            SELECT 1 FROM payment_drafts AS draft
            WHERE draft.invoiceId = invoice.entityId AND draft.status NOT IN ('conflict', 'rejected')
          )
          AND NOT EXISTS (
            SELECT 1 FROM business_documents AS payment
            WHERE payment.entityType = 'payment' AND payment.parentId = invoice.entityId
          )
        LIMIT 1
    """)
    suspend fun payableInvoice(invoiceId: String): PayableInvoice?
}
