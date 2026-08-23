package com.catalogodigital.seller.sync

import java.math.BigDecimal

data class CatalogFeedPage(
    val changes: List<CatalogFeedChange>,
    val nextCursor: Long,
    val hasMore: Boolean,
)

data class CatalogFeedChange(
    val sequence: Long,
    val entityType: String,
    val entityId: String,
    val version: Long,
    val data: Map<String, Any?>,
)

object FeedVersionPolicy {
    fun shouldApply(localVersion: Long?, remoteVersion: Long): Boolean =
        localVersion == null || remoteVersion > localVersion
}

object CatalogFeedPolicy {
    fun requireValid(currentCursor: Long, page: CatalogFeedPage) {
        require(page.nextCursor >= currentCursor) { "The catalog cursor cannot move backwards." }
        var previous = currentCursor
        page.changes.forEach { change ->
            require(change.sequence > previous) { "Catalog change sequences must increase." }
            require(change.sequence <= page.nextCursor) { "A change cannot exceed the page cursor." }
            require(change.entityType == "customer" || change.entityType == "product") {
                "The catalog entity type is unsupported."
            }
            require(change.entityId == change.data.string("id")) { "The catalog entity ID is inconsistent." }
            require(change.version == change.data.long("version")) { "The catalog entity version is inconsistent." }
            previous = change.sequence
        }
        require(page.changes.isNotEmpty() || page.nextCursor == currentCursor) {
            "An empty page cannot advance the cursor."
        }
    }
}

object MoneyParser {
    fun toMinorUnits(value: String): Long = BigDecimal(value)
        .setScale(2)
        .movePointRight(2)
        .longValueExact()
        .also { require(it >= 0) { "Money cannot be negative." } }
}

internal fun Map<String, Any?>.string(key: String): String = this[key] as? String
    ?: throw IllegalArgumentException("Missing string field: $key")

internal fun Map<String, Any?>.nullableString(key: String): String? = when (val value = this[key]) {
    null -> null
    is String -> value
    else -> throw IllegalArgumentException("Invalid string field: $key")
}

internal fun Map<String, Any?>.long(key: String): Long = (this[key] as? Number)?.toLong()
    ?: throw IllegalArgumentException("Missing numeric field: $key")

internal fun Map<String, Any?>.boolean(key: String): Boolean = this[key] as? Boolean
    ?: throw IllegalArgumentException("Missing boolean field: $key")
