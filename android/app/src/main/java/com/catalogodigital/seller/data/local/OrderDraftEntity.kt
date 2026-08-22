package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

object LocalOrderStatus {
    const val PENDING = "pending"
    const val APPLIED = "applied"
    const val CONFLICT = "conflict"
    const val REJECTED = "rejected"
}

@Entity(
    tableName = "order_drafts",
    indices = [Index("customerId"), Index("status")],
)
data class OrderDraftEntity(
    @PrimaryKey val id: String,
    val customerId: String,
    val status: String,
    val totalMinor: Long,
    val clientCreatedAt: String,
)
