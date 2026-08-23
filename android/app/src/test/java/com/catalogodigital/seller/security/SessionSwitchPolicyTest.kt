package com.catalogodigital.seller.security

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test

class SessionSwitchPolicyTest {
    @Test
    fun keepsDataForSameSellerEvenWithPendingWork() {
        assertEquals(
            SessionSwitchAction.KEEP_DATA,
            SessionSwitchPolicy.action("seller-1", "seller-1", 3),
        )
    }

    @Test
    fun blocksDifferentOrUnidentifiedSellerWhenWorkIsUnresolved() {
        assertEquals(
            SessionSwitchAction.BLOCK,
            SessionSwitchPolicy.action("seller-1", "seller-2", 1),
        )
        assertEquals(
            SessionSwitchAction.BLOCK,
            SessionSwitchPolicy.action(null, "seller-1", 1),
        )
    }

    @Test
    fun clearsClosedCacheBeforeAssociatingAnotherSeller() {
        assertEquals(
            SessionSwitchAction.CLEAR_DATA,
            SessionSwitchPolicy.action("seller-1", "seller-2", 0),
        )
    }

    @Test
    fun rejectsInvalidPolicyInputs() {
        assertThrows(IllegalArgumentException::class.java) {
            SessionSwitchPolicy.action("seller-1", "", 0)
        }
        assertThrows(IllegalArgumentException::class.java) {
            SessionSwitchPolicy.action("seller-1", "seller-1", -1)
        }
    }
}
