package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "business_documents",
    indices = [Index("entityType"), Index("status"), Index("occurredAt")],
)
data class BusinessDocumentEntity(
    @PrimaryKey val documentKey: String,
    val entityType: String,
    val entityId: String,
    val version: Long,
    val status: String?,
    val amountMinor: Long?,
    val occurredAt: String,
    val encryptedData: ByteArray,
    val dataIv: ByteArray,
)
