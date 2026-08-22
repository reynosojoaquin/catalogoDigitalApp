package com.catalogodigital.seller.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(entities = [PendingOperation::class, SyncCursor::class], version = 1, exportSchema = true)
abstract class CatalogDatabase : RoomDatabase() {
    abstract fun pendingOperationDao(): PendingOperationDao

    companion object {
        fun create(context: Context): CatalogDatabase = Room.databaseBuilder(
            context.applicationContext,
            CatalogDatabase::class.java,
            "catalog-digital.db",
        ).build()
    }
}
