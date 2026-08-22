package com.catalogodigital.seller.sync

import org.junit.Assert.assertEquals
import org.junit.Assert.assertThrows
import org.junit.Test
import java.util.UUID

class CatalogFeedPolicyTest {
    @Test
    fun acceptsMonotonicPageWithMatchingIdentityAndVersion() {
        val change = change(sequence = 4, version = 2)
        CatalogFeedPolicy.requireValid(
            currentCursor = 3,
            page = CatalogFeedPage(listOf(change), nextCursor = 4, hasMore = false),
        )
    }

    @Test
    fun rejectsCursorRollback() {
        assertThrows(IllegalArgumentException::class.java) {
            CatalogFeedPolicy.requireValid(2, CatalogFeedPage(emptyList(), 1, false))
        }
    }

    @Test
    fun rejectsInconsistentEntityVersion() {
        val change = change(sequence = 1, version = 2).copy(version = 3)
        assertThrows(IllegalArgumentException::class.java) {
            CatalogFeedPolicy.requireValid(0, CatalogFeedPage(listOf(change), 1, false))
        }
    }

    @Test
    fun convertsDecimalMoneyWithoutFloatingPoint() {
        assertEquals(1234L, MoneyParser.toMinorUnits("12.34"))
    }

    @Test
    fun rejectsNegativeMoney() {
        assertThrows(IllegalArgumentException::class.java) {
            MoneyParser.toMinorUnits("-0.01")
        }
    }

    private fun change(sequence: Long, version: Long): CatalogFeedChange {
        val id = UUID.randomUUID().toString()
        return CatalogFeedChange(
            sequence = sequence,
            entityType = "customer",
            entityId = id,
            version = version,
            data = mapOf("id" to id, "version" to version),
        )
    }
}
