package com.catalogodigital.seller.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.UUID

class ReturnDraftPolicyTest {
    @Test
    fun calculatesReturnAndCommissionTotalsWithoutFloatingPoint() {
        val source = source(available = 3, price = 2500, commission = 200)
        val items = listOf(ReturnLineInput(source.invoiceItemId, 2))
        val available = mapOf(source.invoiceItemId to source)

        assertEquals(5000L, ReturnDraftPolicy.total(items, available))
        assertEquals(400L, ReturnDraftPolicy.commissionTotal(items, available))
    }

    @Test
    fun rejectsQuantityAboveAvailable() {
        val source = source(available = 1)
        assertThrows(IllegalArgumentException::class.java) {
            ReturnDraftPolicy.validate(
                listOf(ReturnLineInput(source.invoiceItemId, 2)),
                mapOf(source.invoiceItemId to source),
            )
        }
    }

    @Test
    fun rejectsRepeatedInvoiceItem() {
        val source = source(available = 3)
        assertThrows(IllegalArgumentException::class.java) {
            ReturnDraftPolicy.validate(
                listOf(ReturnLineInput(source.invoiceItemId, 1), ReturnLineInput(source.invoiceItemId, 1)),
                mapOf(source.invoiceItemId to source),
            )
        }
    }

    private fun source(
        available: Int,
        price: Long = 1,
        commission: Long = 0,
    ) = ReturnableInvoiceItem(
        invoiceItemId = UUID.randomUUID().toString(),
        productName = UUID.randomUUID().toString(),
        availableQuantity = available,
        unitPriceMinor = price,
        unitCommissionMinor = commission,
    )
}
