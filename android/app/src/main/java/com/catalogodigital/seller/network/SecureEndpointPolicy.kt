package com.catalogodigital.seller.network

object SecureEndpointPolicy {
    fun requireValid(baseUrl: String) {
        require(baseUrl.startsWith("https://")) { "The API URL must use HTTPS." }
        require(baseUrl.removePrefix("https://").isNotBlank()) { "The API URL must include a host." }
    }
}
