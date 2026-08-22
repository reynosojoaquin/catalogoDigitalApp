package com.catalogodigital.seller.data

import androidx.room.withTransaction
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.data.local.CustomerEntity
import com.catalogodigital.seller.data.local.ProductEntity
import com.catalogodigital.seller.data.local.SyncCursor
import com.catalogodigital.seller.sync.CatalogFeedPage
import com.catalogodigital.seller.sync.CatalogFeedPolicy
import com.catalogodigital.seller.sync.MoneyParser
import com.catalogodigital.seller.sync.boolean
import com.catalogodigital.seller.sync.long
import com.catalogodigital.seller.sync.nullableString
import com.catalogodigital.seller.sync.string

class CatalogFeedRepository(private val database: CatalogDatabase) {
    suspend fun cursor(): Long = database.syncCursorDao().sequence(FEED) ?: 0

    suspend fun apply(page: CatalogFeedPage) = database.withTransaction {
        val currentCursor = cursor()
        CatalogFeedPolicy.requireValid(currentCursor, page)
        val dao = database.catalogDao()
        page.changes.forEach { change ->
            if (change.entityType == "customer") {
                if ((dao.customerVersion(change.entityId) ?: 0) <= change.version) {
                    dao.upsertCustomer(CustomerEntity(
                        id = change.data.string("id"),
                        fullName = change.data.string("full_name"),
                        email = change.data.nullableString("email"),
                        phone = change.data.nullableString("phone"),
                        isActive = change.data.boolean("is_active"),
                        version = change.data.long("version"),
                        updatedAt = change.data.string("updated_at"),
                    ))
                }
            } else {
                if ((dao.productVersion(change.entityId) ?: 0) <= change.version) {
                    dao.upsertProduct(ProductEntity(
                        id = change.data.string("id"),
                        sku = change.data.string("sku"),
                        name = change.data.string("name"),
                        description = change.data.string("description"),
                        priceMinor = MoneyParser.toMinorUnits(change.data.string("price")),
                        commissionMinor = MoneyParser.toMinorUnits(change.data.string("commission_amount")),
                        isActive = change.data.boolean("is_active"),
                        version = change.data.long("version"),
                        updatedAt = change.data.string("updated_at"),
                    ))
                }
            }
        }
        database.syncCursorDao().upsert(SyncCursor(FEED, page.nextCursor))
    }

    private companion object {
        const val FEED = "catalog"
    }
}
