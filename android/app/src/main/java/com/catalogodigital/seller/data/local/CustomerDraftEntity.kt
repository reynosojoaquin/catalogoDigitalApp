package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey
import androidx.room.ColumnInfo

@Entity(
    tableName = "customer_drafts",
    indices = [
        Index(value = ["email"], unique = true),
        Index(value = ["phone"], unique = true),
        Index(value = ["identityFingerprint"], unique = true),
    ],
)
data class CustomerDraftEntity(
    @PrimaryKey val id: String,
    val fullName: String,
    val email: String?,
    val phone: String?,
    val identityFingerprint: ByteArray?,
    val createdAt: String,
    @ColumnInfo(defaultValue = "'pending'") val status: String = OperationStatus.PENDING,
)
