package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index

@Entity(
    tableName = "return_draft_items",
    primaryKeys = ["returnId", "invoiceItemId"],
    foreignKeys = [ForeignKey(
        entity = ReturnDraftEntity::class,
        parentColumns = ["id"],
        childColumns = ["returnId"],
        onDelete = ForeignKey.RESTRICT,
    )],
    indices = [Index("returnId"), Index("invoiceItemId")],
)
data class ReturnDraftItemEntity(
    val returnId: String,
    val invoiceItemId: String,
    val productName: String,
    val quantity: Int,
    val unitPriceMinor: Long,
    val unitCommissionMinor: Long,
    val lineTotalMinor: Long,
    val commissionTotalMinor: Long,
)
