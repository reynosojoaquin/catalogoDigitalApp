package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sync_cursors")
data class SyncCursor(
    @PrimaryKey val feed: String,
    val sequence: Long,
)
