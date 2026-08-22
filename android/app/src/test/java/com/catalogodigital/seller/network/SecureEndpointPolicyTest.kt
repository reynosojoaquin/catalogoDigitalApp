package com.catalogodigital.seller.network

import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.UUID

class SecureEndpointPolicyTest {
    @Test
    fun acceptsHttpsEndpoint() {
        SecureEndpointPolicy.requireValid("https://${UUID.randomUUID()}.invalid")
    }

    @Test
    fun rejectsCleartextEndpoint() {
        assertThrows(IllegalArgumentException::class.java) {
            SecureEndpointPolicy.requireValid("http://${UUID.randomUUID()}.invalid")
        }
    }

    @Test
    fun rejectsEndpointWithoutHost() {
        assertThrows(IllegalArgumentException::class.java) {
            SecureEndpointPolicy.requireValid("https://")
        }
    }
}
