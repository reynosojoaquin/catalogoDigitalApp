package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "products",
    indices = [Index(value = ["sku"], unique = true), Index("name"), Index("isActive")],
)
data class ProductEntity(
    @PrimaryKey val id: String,
    val sku: String,
    val name: String,
    val description: String,
    val priceMinor: Long,
    val commissionMinor: Long,
    val isActive: Boolean,
    val version: Long,
    val updatedAt: String,
)
