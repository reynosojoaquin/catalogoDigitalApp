package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

@Entity(
    tableName = "payment_drafts",
    indices = [Index("invoiceId"), Index("status")],
)
data class PaymentDraftEntity(
    @PrimaryKey val id: String,
    val invoiceId: String,
    val method: String,
    val status: String,
    val amountMinor: Long,
    val clientReportedAt: String,
)
