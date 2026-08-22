package com.catalogodigital.seller.data

object PaymentMethod {
    const val CASH = "cash"
    const val EXTERNAL_CARD_TERMINAL = "external_card_terminal"
}

data class NormalizedPaymentInput(val method: String, val terminalReference: String?)

object PaymentInputPolicy {
    fun normalize(method: String, terminalReference: String?): NormalizedPaymentInput {
        require(method == PaymentMethod.CASH || method == PaymentMethod.EXTERNAL_CARD_TERMINAL) {
            "The payment method is unsupported."
        }
        val reference = terminalReference?.trim()?.ifEmpty { null }
        require(reference == null || reference.length <= 120) { "The terminal reference is too long." }
        require(method != PaymentMethod.CASH || reference == null) {
            "Cash payments cannot include a terminal reference."
        }
        require(method != PaymentMethod.EXTERNAL_CARD_TERMINAL || reference != null) {
            "A terminal reference is required."
        }
        require(reference == null || !looksLikeCardNumber(reference)) {
            "Card numbers cannot be used as terminal references."
        }
        return NormalizedPaymentInput(method, reference)
    }

    fun looksLikeCardNumber(value: String): Boolean {
        val digits = value.filter(Char::isDigit)
        if (digits.length !in 13..19) return false
        var checksum = 0
        val parity = digits.length % 2
        digits.forEachIndexed { index, character ->
            var number = character.digitToInt()
            if (index % 2 == parity) {
                number *= 2
                if (number > 9) number -= 9
            }
            checksum += number
        }
        return checksum % 10 == 0
    }
}
