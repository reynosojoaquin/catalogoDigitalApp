package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.data.local.PayableInvoice
import com.catalogodigital.seller.data.local.PaymentDraftEntity
import org.json.JSONObject
import java.time.Instant
import java.util.UUID

class OfflinePaymentRepository(private val database: CatalogDatabase) {
    suspend fun payableInvoices(): List<PayableInvoice> = database.paymentDraftDao().payableInvoices()

    suspend fun create(
        deviceId: UUID,
        invoiceId: String,
        method: String,
        terminalReference: String?,
    ): UUID {
        val input = PaymentInputPolicy.normalize(method, terminalReference)
        val reportId = UUID.randomUUID()
        val reportedAt = Instant.now().toString()
        database.withTransaction {
            val invoice = requireNotNull(database.paymentDraftDao().payableInvoice(invoiceId)) {
                "The invoice is no longer payable."
            }
            val payload = JSONObject()
                .put("id", reportId.toString())
                .put("invoice_id", invoice.id)
                .put("method", input.method)
                .put("external_terminal_reference", input.terminalReference ?: JSONObject.NULL)
                .put("client_reported_at", reportedAt)
            val operation = OperationQueue(database.pendingOperationDao()).build(
                "payment_create", reportId, deviceId, payload.toString(),
            )
            database.paymentDraftDao().insert(PaymentDraftEntity(
                id = reportId.toString(),
                invoiceId = invoice.id,
                method = input.method,
                status = OperationStatus.PENDING,
                amountMinor = invoice.amountMinor,
                clientReportedAt = reportedAt,
            ))
            database.pendingOperationDao().insert(operation)
        }
        return reportId
    }
}
