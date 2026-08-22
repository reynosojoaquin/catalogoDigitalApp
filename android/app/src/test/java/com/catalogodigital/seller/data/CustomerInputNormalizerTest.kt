package com.catalogodigital.seller.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.Locale
import java.util.UUID

class CustomerInputNormalizerTest {
    @Test
    fun normalizesWhitespaceEmailAndPhoneLikeServerContract() {
        val localPart = UUID.randomUUID().toString().uppercase(Locale.ROOT)
        val input = CustomerInputNormalizer.normalize(
            fullName = "  $localPart   $localPart  ",
            email = " $localPart@INVALID ",
            phone = " +(809) + 000-0000 ",
            identity = null,
        )

        assertEquals("$localPart $localPart", input.fullName)
        assertEquals("${localPart.lowercase(Locale.ROOT)}@invalid", input.email)
        assertEquals("+8090000000", input.phone)
        assertNull(input.identity)
    }

    @Test
    fun normalizesIdentityForLocalFingerprint() {
        val source = UUID.randomUUID().toString()
        val input = CustomerInputNormalizer.normalize(source, null, null, source)

        assertEquals(source.replace("-", "").lowercase(Locale.ROOT), input.identity)
    }

    @Test
    fun requiresAtLeastOneIdentifier() {
        assertThrows(IllegalArgumentException::class.java) {
            CustomerInputNormalizer.normalize(UUID.randomUUID().toString(), null, " ", null)
        }
    }
}
