package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.BusinessDocumentEntity
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.data.local.ReturnDraftEntity
import com.catalogodigital.seller.data.local.ReturnDraftItemEntity
import com.catalogodigital.seller.security.EncryptedValue
import com.catalogodigital.seller.security.KeystoreCipher
import com.catalogodigital.seller.sync.MoneyParser
import org.json.JSONArray
import org.json.JSONObject
import java.time.Instant
import java.util.UUID

data class ReturnableInvoice(
    val id: String,
    val label: String,
    val items: List<ReturnableInvoiceItem>,
)

class OfflineReturnRepository(
    private val database: CatalogDatabase,
    private val cipher: KeystoreCipher = KeystoreCipher(),
) {
    suspend fun returnableInvoices(): List<ReturnableInvoice> = buildReturnableInvoices()

    suspend fun create(
        deviceId: UUID,
        invoiceId: String,
        items: List<ReturnLineInput>,
    ): UUID = database.withTransaction {
        val invoice = requireNotNull(buildReturnableInvoices().firstOrNull { it.id == invoiceId }) {
            "The invoice is unavailable for returns."
        }
        val available = invoice.items.associateBy(ReturnableInvoiceItem::invoiceItemId)
        ReturnDraftPolicy.validate(items, available)
        val reportId = UUID.randomUUID()
        val reportedAt = Instant.now().toString()
        val payload = JSONObject()
            .put("id", reportId.toString())
            .put("invoice_id", invoice.id)
            .put("client_reported_at", reportedAt)
            .put("items", JSONArray().apply {
                items.forEach { item ->
                    put(JSONObject().put("invoice_item_id", item.invoiceItemId).put("quantity", item.quantity))
                }
            })
        val operation = OperationQueue(database.pendingOperationDao()).build(
            "return_create", reportId, deviceId, payload.toString(),
        )
        database.returnDraftDao().insertReturn(ReturnDraftEntity(
            id = reportId.toString(),
            invoiceId = invoice.id,
            status = OperationStatus.PENDING,
            totalMinor = ReturnDraftPolicy.total(items, available),
            commissionTotalMinor = ReturnDraftPolicy.commissionTotal(items, available),
            clientReportedAt = reportedAt,
        ))
        database.returnDraftDao().insertItems(items.map { item ->
            val source = available.getValue(item.invoiceItemId)
            ReturnDraftItemEntity(
                returnId = reportId.toString(),
                invoiceItemId = item.invoiceItemId,
                productName = source.productName,
                quantity = item.quantity,
                unitPriceMinor = source.unitPriceMinor,
                unitCommissionMinor = source.unitCommissionMinor,
                lineTotalMinor = Math.multiplyExact(source.unitPriceMinor, item.quantity.toLong()),
                commissionTotalMinor = Math.multiplyExact(source.unitCommissionMinor, item.quantity.toLong()),
            )
        })
        database.pendingOperationDao().insert(operation)
        reportId
    }

    private suspend fun buildReturnableInvoices(): List<ReturnableInvoice> {
        val synchronizedReturned = mutableMapOf<String, Long>()
        database.businessDocumentDao().byType("return").forEach { document ->
            val data = decrypt(document)
            val items = data.getJSONArray("items")
            repeat(items.length()) { index ->
                val item = items.getJSONObject(index)
                val id = item.getString("invoice_item_id")
                synchronizedReturned[id] = Math.addExact(
                    synchronizedReturned[id] ?: 0,
                    item.getLong("quantity"),
                )
            }
        }
        val localReturned = database.returnDraftDao().returnedQuantities()
            .associate { it.invoiceItemId to it.quantity }
        return database.businessDocumentDao().byTypeAndStatus("invoice", "paid").mapNotNull { document ->
            val data = decrypt(document)
            val sourceItems = data.getJSONArray("items")
            val items = buildList {
                repeat(sourceItems.length()) { index ->
                    val item = sourceItems.getJSONObject(index)
                    val id = item.getString("id")
                    val used = Math.addExact(synchronizedReturned[id] ?: 0, localReturned[id] ?: 0)
                    val available = item.getLong("quantity") - used
                    if (available > 0) {
                        require(available <= Int.MAX_VALUE) { "The available return quantity is too large." }
                        add(ReturnableInvoiceItem(
                            invoiceItemId = id,
                            productName = item.getString("product_name"),
                            availableQuantity = available.toInt(),
                            unitPriceMinor = MoneyParser.toMinorUnits(item.getString("unit_price")),
                            unitCommissionMinor = MoneyParser.toMinorUnits(item.getString("unit_commission")),
                        ))
                    }
                }
            }
            if (items.isEmpty()) null else ReturnableInvoice(
                id = document.entityId,
                label = data.optString("customer_name").ifBlank { document.entityId },
                items = items,
            )
        }
    }

    private fun decrypt(document: BusinessDocumentEntity): JSONObject = JSONObject(
        cipher.decrypt(EncryptedValue(document.encryptedData, document.dataIv)).decodeToString(),
    )
}
