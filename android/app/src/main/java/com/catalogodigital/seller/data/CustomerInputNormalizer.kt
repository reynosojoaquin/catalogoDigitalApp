package com.catalogodigital.seller.data

import java.util.Locale

data class NormalizedCustomerInput(
    val fullName: String,
    val email: String?,
    val phone: String?,
    val identity: String?,
)

object CustomerInputNormalizer {
    fun normalize(fullName: String, email: String?, phone: String?, identity: String?): NormalizedCustomerInput {
        val normalizedName = fullName.trim().split(Regex("\\s+")).filter(String::isNotEmpty).joinToString(" ")
        require(normalizedName.isNotEmpty()) { "Customer name is required." }
        val normalizedEmail = email?.trim()?.lowercase(Locale.ROOT)?.ifEmpty { null }
        val normalizedPhone = phone?.trim()
            ?.replace(Regex("[^0-9+]"), "")
            ?.let { value ->
                if (value.startsWith("+")) "+" + value.drop(1).replace("+", "") else value.replace("+", "")
            }
            ?.ifEmpty { null }
        val normalizedIdentity = identity?.replace(Regex("[^0-9A-Za-z]"), "")
            ?.lowercase(Locale.ROOT)
            ?.ifEmpty { null }
        require(normalizedEmail != null || normalizedPhone != null || normalizedIdentity != null) {
            "At least one customer identifier is required."
        }
        return NormalizedCustomerInput(normalizedName, normalizedEmail, normalizedPhone, normalizedIdentity)
    }
}
