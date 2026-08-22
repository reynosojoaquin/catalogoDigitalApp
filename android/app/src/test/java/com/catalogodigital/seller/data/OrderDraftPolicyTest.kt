package com.catalogodigital.seller.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.UUID

class OrderDraftPolicyTest {
    @Test
    fun calculatesTotalsWithIntegerMinorUnits() {
        val lines = listOf(line(price = 125, quantity = 2), line(price = 50, quantity = 3))

        assertEquals(400L, OrderDraftPolicy.total(lines))
    }

    @Test
    fun rejectsDuplicateProducts() {
        val productId = UUID.randomUUID().toString()
        assertThrows(IllegalArgumentException::class.java) {
            OrderDraftPolicy.validateInputs(
                listOf(OrderLineInput(productId, 1), OrderLineInput(productId, 2)),
            )
        }
    }

    @Test
    fun rejectsNonPositiveQuantity() {
        assertThrows(IllegalArgumentException::class.java) {
            OrderDraftPolicy.validateInputs(listOf(OrderLineInput(UUID.randomUUID().toString(), 0)))
        }
    }

    @Test
    fun failsOnMonetaryOverflow() {
        assertThrows(ArithmeticException::class.java) {
            OrderDraftPolicy.total(listOf(line(Long.MAX_VALUE, 2)))
        }
    }

    private fun line(price: Long, quantity: Int) = PricedOrderLine(
        productId = UUID.randomUUID().toString(),
        productSku = UUID.randomUUID().toString(),
        productName = UUID.randomUUID().toString(),
        unitPriceMinor = price,
        unitCommissionMinor = 0,
        quantity = quantity,
    )
}
