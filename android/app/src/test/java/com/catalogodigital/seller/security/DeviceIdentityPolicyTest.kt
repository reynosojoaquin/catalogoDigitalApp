package com.catalogodigital.seller.security

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import java.util.UUID

class DeviceIdentityPolicyTest {
    @Test
    fun parsesStoredUuid() {
        val expected = UUID.randomUUID()

        assertEquals(expected, DeviceIdentityPolicy.parseStored(expected.toString()))
    }

    @Test
    fun ignoresCorruptedOrMissingStoredValue() {
        assertNull(DeviceIdentityPolicy.parseStored("corrupted-device-id"))
        assertNull(DeviceIdentityPolicy.parseStored(null))
    }
}
