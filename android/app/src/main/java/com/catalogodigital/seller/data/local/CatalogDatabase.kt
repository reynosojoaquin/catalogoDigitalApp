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
        ProductEntity::class, CustomerDraftEntity::class, OrderDraftEntity::class,
        OrderDraftItemEntity::class, BusinessDocumentEntity::class, PaymentDraftEntity::class,
        ReturnDraftEntity::class, ReturnDraftItemEntity::class,
    ],
    version = 8,
    exportSchema = true,
)
abstract class CatalogDatabase : RoomDatabase() {
    abstract fun pendingOperationDao(): PendingOperationDao
    abstract fun catalogDao(): CatalogDao
    abstract fun syncCursorDao(): SyncCursorDao
    abstract fun customerDraftDao(): CustomerDraftDao
    abstract fun orderDraftDao(): OrderDraftDao
    abstract fun businessDocumentDao(): BusinessDocumentDao
    abstract fun paymentDraftDao(): PaymentDraftDao
    abstract fun returnDraftDao(): ReturnDraftDao

    companion object {
        fun create(context: Context): CatalogDatabase = Room.databaseBuilder(
            context.applicationContext,
            CatalogDatabase::class.java,
            "catalog-digital.db",
        ).addMigrations(
            MIGRATION_1_2, MIGRATION_2_3, MIGRATION_3_4, MIGRATION_4_5, MIGRATION_5_6,
            MIGRATION_6_7,
            MIGRATION_7_8,
        ).build()

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

        private val MIGRATION_3_4 = object : Migration(3, 4) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `order_drafts` (`id` TEXT NOT NULL, `customerId` TEXT NOT NULL, `status` TEXT NOT NULL, `totalMinor` INTEGER NOT NULL, `clientCreatedAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_order_drafts_customerId` ON `order_drafts` (`customerId`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_order_drafts_status` ON `order_drafts` (`status`)")
                db.execSQL("CREATE TABLE IF NOT EXISTS `order_draft_items` (`orderId` TEXT NOT NULL, `productId` TEXT NOT NULL, `productSku` TEXT NOT NULL, `productName` TEXT NOT NULL, `unitPriceMinor` INTEGER NOT NULL, `unitCommissionMinor` INTEGER NOT NULL, `quantity` INTEGER NOT NULL, `lineTotalMinor` INTEGER NOT NULL, PRIMARY KEY(`orderId`, `productId`), FOREIGN KEY(`orderId`) REFERENCES `order_drafts`(`id`) ON UPDATE NO ACTION ON DELETE RESTRICT )")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_order_draft_items_orderId` ON `order_draft_items` (`orderId`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_order_draft_items_productId` ON `order_draft_items` (`productId`)")
            }
        }

        private val MIGRATION_4_5 = object : Migration(4, 5) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("ALTER TABLE `pending_operations` ADD COLUMN `entityId` TEXT")
                db.execSQL("ALTER TABLE `customer_drafts` ADD COLUMN `status` TEXT NOT NULL DEFAULT 'pending'")
            }
        }

        private val MIGRATION_5_6 = object : Migration(5, 6) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `business_documents` (`documentKey` TEXT NOT NULL, `entityType` TEXT NOT NULL, `entityId` TEXT NOT NULL, `version` INTEGER NOT NULL, `status` TEXT, `amountMinor` INTEGER, `occurredAt` TEXT NOT NULL, `encryptedData` BLOB NOT NULL, `dataIv` BLOB NOT NULL, PRIMARY KEY(`documentKey`))")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_business_documents_entityType` ON `business_documents` (`entityType`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_business_documents_status` ON `business_documents` (`status`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_business_documents_occurredAt` ON `business_documents` (`occurredAt`)")
            }
        }

        private val MIGRATION_6_7 = object : Migration(6, 7) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("ALTER TABLE `business_documents` ADD COLUMN `parentId` TEXT")
                db.execSQL("ALTER TABLE `business_documents` ADD COLUMN `displayLabel` TEXT")
                db.execSQL("CREATE TABLE IF NOT EXISTS `payment_drafts` (`id` TEXT NOT NULL, `invoiceId` TEXT NOT NULL, `method` TEXT NOT NULL, `status` TEXT NOT NULL, `amountMinor` INTEGER NOT NULL, `clientReportedAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_payment_drafts_invoiceId` ON `payment_drafts` (`invoiceId`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_payment_drafts_status` ON `payment_drafts` (`status`)")
                db.execSQL("UPDATE `sync_cursors` SET `sequence` = 0 WHERE `feed` = 'business'")
            }
        }

        private val MIGRATION_7_8 = object : Migration(7, 8) {
            override fun migrate(db: SupportSQLiteDatabase) {
                db.execSQL("CREATE TABLE IF NOT EXISTS `return_drafts` (`id` TEXT NOT NULL, `invoiceId` TEXT NOT NULL, `status` TEXT NOT NULL, `totalMinor` INTEGER NOT NULL, `commissionTotalMinor` INTEGER NOT NULL, `clientReportedAt` TEXT NOT NULL, PRIMARY KEY(`id`))")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_return_drafts_invoiceId` ON `return_drafts` (`invoiceId`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_return_drafts_status` ON `return_drafts` (`status`)")
                db.execSQL("CREATE TABLE IF NOT EXISTS `return_draft_items` (`returnId` TEXT NOT NULL, `invoiceItemId` TEXT NOT NULL, `productName` TEXT NOT NULL, `quantity` INTEGER NOT NULL, `unitPriceMinor` INTEGER NOT NULL, `unitCommissionMinor` INTEGER NOT NULL, `lineTotalMinor` INTEGER NOT NULL, `commissionTotalMinor` INTEGER NOT NULL, PRIMARY KEY(`returnId`, `invoiceItemId`), FOREIGN KEY(`returnId`) REFERENCES `return_drafts`(`id`) ON UPDATE NO ACTION ON DELETE RESTRICT )")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_return_draft_items_returnId` ON `return_draft_items` (`returnId`)")
                db.execSQL("CREATE INDEX IF NOT EXISTS `index_return_draft_items_invoiceItemId` ON `return_draft_items` (`invoiceItemId`)")
            }
        }
    }
}
