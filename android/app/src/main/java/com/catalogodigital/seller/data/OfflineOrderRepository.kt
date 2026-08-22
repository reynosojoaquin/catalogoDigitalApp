package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.CustomerOption
import com.catalogodigital.seller.data.local.LocalOrderStatus
import com.catalogodigital.seller.data.local.OrderDraftEntity
import com.catalogodigital.seller.data.local.OrderDraftItemEntity
import com.catalogodigital.seller.data.local.ProductEntity
import org.json.JSONArray
import org.json.JSONObject
import java.time.Instant
import java.util.UUID

class OfflineOrderRepository(private val database: CatalogDatabase) {
    suspend fun availableCustomers(): List<CustomerOption> = database.orderDraftDao().availableCustomers()

    suspend fun availableProducts(): List<ProductEntity> = database.orderDraftDao().availableProducts()

    suspend fun create(deviceId: UUID, customerId: String, items: List<OrderLineInput>): UUID {
        OrderDraftPolicy.validateInputs(items)
        val orderId = UUID.randomUUID()
        val createdAt = Instant.now().toString()

        database.withTransaction {
            val dao = database.orderDraftDao()
            require(dao.customerIsAvailable(customerId)) { "The selected customer is unavailable." }
            val products = dao.activeProductsByIds(items.map(OrderLineInput::productId))
                .associateBy(ProductEntity::id)
            require(products.size == items.size) { "One or more selected products are unavailable." }
            val pricedLines = items.map { item ->
                val product = requireNotNull(products[item.productId])
                PricedOrderLine(
                    productId = product.id,
                    productSku = product.sku,
                    productName = product.name,
                    unitPriceMinor = product.priceMinor,
                    unitCommissionMinor = product.commissionMinor,
                    quantity = item.quantity,
                )
            }
            val total = OrderDraftPolicy.total(pricedLines)
            val payload = JSONObject()
                .put("id", orderId.toString())
                .put("customer_id", customerId)
                .put("client_created_at", createdAt)
                .put("items", JSONArray().apply {
                    pricedLines.forEach { line ->
                        put(JSONObject().put("product_id", line.productId).put("quantity", line.quantity))
                    }
                })
            val operation = OperationQueue(database.pendingOperationDao())
                .build("order_create", deviceId, payload.toString())

            dao.insertOrder(OrderDraftEntity(
                id = orderId.toString(),
                customerId = customerId,
                status = LocalOrderStatus.PENDING,
                totalMinor = total,
                clientCreatedAt = createdAt,
            ))
            dao.insertItems(pricedLines.map { line ->
                OrderDraftItemEntity(
                    orderId = orderId.toString(),
                    productId = line.productId,
                    productSku = line.productSku,
                    productName = line.productName,
                    unitPriceMinor = line.unitPriceMinor,
                    unitCommissionMinor = line.unitCommissionMinor,
                    quantity = line.quantity,
                    lineTotalMinor = OrderDraftPolicy.lineTotal(line),
                )
            })
            database.pendingOperationDao().insert(operation)
        }
        return orderId
    }
}
