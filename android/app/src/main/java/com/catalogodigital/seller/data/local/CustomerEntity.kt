package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "customers",
    indices = [Index("fullName"), Index("isActive")],
)
data class CustomerEntity(
    @PrimaryKey val id: String,
    val fullName: String,
    val email: String?,
    val phone: String?,
    val isActive: Boolean,
    val version: Long,
    val updatedAt: String,
)
