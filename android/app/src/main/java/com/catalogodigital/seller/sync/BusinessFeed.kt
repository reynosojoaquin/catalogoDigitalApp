package com.catalogodigital.seller.sync

data class BusinessFeedPage(
    val changes: List<BusinessFeedChange>,
    val nextCursor: Long,
    val hasMore: Boolean,
)

data class BusinessFeedChange(
    val sequence: Long,
    val entityType: String,
    val entityId: String,
    val version: Long,
    val occurredAt: String,
    val dataId: String,
    val dataVersion: Long?,
    val dataJson: String,
)

object BusinessFeedPolicy {
    val supportedTypes = setOf("order", "invoice", "payment", "return", "commission", "settlement")

    fun requireValid(currentCursor: Long, page: BusinessFeedPage) {
        require(page.nextCursor >= currentCursor) { "The business cursor cannot move backwards." }
        var previous = currentCursor
        page.changes.forEach { change ->
            require(change.sequence > previous) { "Business change sequences must increase." }
            require(change.sequence <= page.nextCursor) { "A change cannot exceed the business cursor." }
            require(change.entityType in supportedTypes) { "The business entity type is unsupported." }
            require(change.entityId == change.dataId) { "The business entity ID is inconsistent." }
            require(change.dataVersion == null || change.dataVersion == change.version) {
                "The business entity version is inconsistent."
            }
            previous = change.sequence
        }
        require(page.changes.isNotEmpty() || page.nextCursor == currentCursor) {
            "An empty business page cannot advance the cursor."
        }
    }
}
