package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "return_drafts",
    indices = [Index("invoiceId"), Index("status")],
)
data class ReturnDraftEntity(
    @PrimaryKey val id: String,
    val invoiceId: String,
    val status: String,
    val totalMinor: Long,
    val commissionTotalMinor: Long,
    val clientReportedAt: String,
)
