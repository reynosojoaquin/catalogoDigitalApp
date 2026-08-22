package com.catalogodigital.seller.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase

@Database(
    entities = [
        PendingOperation::class, SyncCursor::class, CustomerEntity::class,
        ProductEntity::class, CustomerDraftEntity::class,
    ],
    version = 3,
    exportSchema = true,
)
abstract class CatalogDatabase : RoomDatabase() {
    abstract fun pendingOperationDao(): PendingOperationDao
    abstract fun catalogDao(): CatalogDao
    abstract fun syncCursorDao(): SyncCursorDao
    abstract fun customerDraftDao(): CustomerDraftDao

    companion object {
        fun create(context: Context): CatalogDatabase = Room.databaseBuilder(
            context.applicationContext,
            CatalogDatabase::class.java,
            "catalog-digital.db",
        ).addMigrations(MIGRATION_1_2, MIGRATION_2_3).build()

        private val MIGRATION_1_2 = object : Migration(1, 2) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `customers` (`id` TEXT NOT NULL, `fullName` TEXT NOT NULL, `email` TEXT, `phone` TEXT, `isActive` INTEGER NOT NULL, `version` INTEGER NOT NULL, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_customers_fullName` ON `customers` (`fullName`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_customers_isActive` ON `customers` (`isActive`)")
                db.execSQL("CREATE TABLE IF NOT EXISTS `products` (`id` TEXT NOT NULL, `sku` TEXT NOT NULL, `name` TEXT NOT NULL, `description` TEXT NOT NULL, `priceMinor` INTEGER NOT NULL, `commissionMinor` INTEGER NOT NULL, `isActive` INTEGER NOT NULL, `version` INTEGER NOT NULL, `updatedAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS `index_products_sku` ON `products` (`sku`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_products_name` ON `products` (`name`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_products_isActive` ON `products` (`isActive`)")
            }
        }

        private val MIGRATION_2_3 = object : Migration(2, 3) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `customer_drafts` (`id` TEXT NOT NULL, `fullName` TEXT NOT NULL, `email` TEXT, `phone` TEXT, `identityFingerprint` BLOB, `createdAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS `index_customer_drafts_email` ON `customer_drafts` (`email`)")
                db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS `index_customer_drafts_phone` ON `customer_drafts` (`phone`)")
                db.execSQL("CREATE UNIQUE INDEX IF NOT EXISTS `index_customer_drafts_identityFingerprint` ON `customer_drafts` (`identityFingerprint`)")
            }
        }
    }
}
