package com.catalogodigital.seller.sync

import org.junit.Assert.assertThrows
import org.junit.Test
import java.time.Instant
import java.util.UUID

class BusinessFeedPolicyTest {
    @Test
    fun acceptsSupportedDocumentWithConsistentIdentityAndVersion() {
        val change = change()
        BusinessFeedPolicy.requireValid(0, BusinessFeedPage(listOf(change), change.sequence, false))
    }

    @Test
    fun acceptsSettlementWithoutDocumentVersion() {
        val change = change().copy(entityType = "settlement", dataVersion = null)
        BusinessFeedPolicy.requireValid(0, BusinessFeedPage(listOf(change), change.sequence, false))
    }

    @Test
    fun rejectsUnknownDocumentType() {
        val change = change().copy(entityType = UUID.randomUUID().toString())
        assertThrows(IllegalArgumentException::class.java) {
            BusinessFeedPolicy.requireValid(0, BusinessFeedPage(listOf(change), change.sequence, false))
        }
    }

    @Test
    fun rejectsDocumentIdentityMismatch() {
        val change = change().copy(dataId = UUID.randomUUID().toString())
        assertThrows(IllegalArgumentException::class.java) {
            BusinessFeedPolicy.requireValid(0, BusinessFeedPage(listOf(change), change.sequence, false))
        }
    }

    @Test
    fun rejectsDocumentVersionMismatch() {
        val change = change().copy(dataVersion = 2)
        assertThrows(IllegalArgumentException::class.java) {
            BusinessFeedPolicy.requireValid(0, BusinessFeedPage(listOf(change), change.sequence, false))
        }
    }

    private fun change(): BusinessFeedChange {
        val id = UUID.randomUUID().toString()
        return BusinessFeedChange(
            sequence = 1,
            entityType = "order",
            entityId = id,
            version = 1,
            occurredAt = Instant.EPOCH.toString(),
            dataId = id,
            dataVersion = 1,
            dataJson = "{}",
        )
    }
}
