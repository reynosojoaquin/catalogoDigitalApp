package com.catalogodigital.seller.data

data class ReturnLineInput(val invoiceItemId: String, val quantity: Int)

data class ReturnableInvoiceItem(
    val invoiceItemId: String,
    val productName: String,
    val availableQuantity: Int,
    val unitPriceMinor: Long,
    val unitCommissionMinor: Long,
)

object ReturnDraftPolicy {
    fun validate(items: List<ReturnLineInput>, available: Map<String, ReturnableInvoiceItem>) {
        require(items.isNotEmpty()) { "A return requires at least one item." }
        require(items.map(ReturnLineInput::invoiceItemId).distinct().size == items.size) {
            "An invoice item can appear only once in a return."
        }
        items.forEach { item ->
            require(item.quantity > 0) { "Return quantities must be positive." }
            val source = requireNotNull(available[item.invoiceItemId]) { "The invoice item is unavailable." }
            require(item.quantity <= source.availableQuantity) { "The return quantity exceeds the available amount." }
        }
    }

    fun total(items: List<ReturnLineInput>, available: Map<String, ReturnableInvoiceItem>): Long =
        items.fold(0L) { total, item ->
            Math.addExact(total, Math.multiplyExact(available.getValue(item.invoiceItemId).unitPriceMinor, item.quantity.toLong()))
        }

    fun commissionTotal(items: List<ReturnLineInput>, available: Map<String, ReturnableInvoiceItem>): Long =
        items.fold(0L) { total, item ->
            Math.addExact(
                total,
                Math.multiplyExact(available.getValue(item.invoiceItemId).unitCommissionMinor, item.quantity.toLong()),
            )
        }
}
