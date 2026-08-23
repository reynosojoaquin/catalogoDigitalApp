package com.catalogodigital.seller.data

import org.junit.Assert.assertNull
import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.UUID

class PaymentInputPolicyTest {
    @Test
    fun acceptsCashWithoutReference() {
        assertNull(PaymentInputPolicy.normalize(PaymentMethod.CASH, null).terminalReference)
    }

    @Test
    fun requiresExternalTerminalReference() {
        assertThrows(IllegalArgumentException::class.java) {
            PaymentInputPolicy.normalize(PaymentMethod.EXTERNAL_CARD_TERMINAL, " ")
        }
    }

    @Test
    fun rejectsReferenceForCash() {
        assertThrows(IllegalArgumentException::class.java) {
            PaymentInputPolicy.normalize(PaymentMethod.CASH, UUID.randomUUID().toString())
        }
    }

    @Test
    fun rejectsCardNumberAsReference() {
        assertThrows(IllegalArgumentException::class.java) {
            PaymentInputPolicy.normalize(PaymentMethod.EXTERNAL_CARD_TERMINAL, validLuhnNumber())
        }
    }

    @Test
    fun rejectsCardLengthReferenceWithoutChecksum() {
        assertThrows(IllegalArgumentException::class.java) {
            PaymentInputPolicy.normalize(
                PaymentMethod.EXTERNAL_CARD_TERMINAL,
                "4111 1111 1111 1112",
            )
        }
    }

    @Test
    fun acceptsOpaqueTerminalReference() {
        PaymentInputPolicy.normalize(
            PaymentMethod.EXTERNAL_CARD_TERMINAL,
            UUID.randomUUID().toString(),
        )
    }

    private fun validLuhnNumber(): String {
        val prefix = UUID.randomUUID().toString().filter(Char::isDigit).padEnd(15, '0').take(15)
        return (0..9).map { "$prefix$it" }.first(PaymentInputPolicy::looksLikeCardNumber)
    }
}
