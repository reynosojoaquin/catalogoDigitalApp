package com.catalogodigital.seller.data

data class OrderLineInput(val productId: String, val quantity: Int)

data class PricedOrderLine(
    val productId: String,
    val productSku: String,
    val productName: String,
    val unitPriceMinor: Long,
    val unitCommissionMinor: Long,
    val quantity: Int,
)

object OrderDraftPolicy {
    fun validateInputs(items: List<OrderLineInput>) {
        require(items.isNotEmpty()) { "An order requires at least one item." }
        require(items.all { it.quantity > 0 }) { "Order quantities must be positive." }
        require(items.map(OrderLineInput::productId).distinct().size == items.size) {
            "A product can appear only once in an order."
        }
    }

    fun lineTotal(line: PricedOrderLine): Long = Math.multiplyExact(line.unitPriceMinor, line.quantity.toLong())

    fun total(lines: List<PricedOrderLine>): Long = lines.fold(0L) { total, line ->
        Math.addExact(total, lineTotal(line))
    }
}
