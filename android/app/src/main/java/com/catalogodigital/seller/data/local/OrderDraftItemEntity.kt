package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index

@Entity(
    tableName = "order_draft_items",
    primaryKeys = ["orderId", "productId"],
    foreignKeys = [ForeignKey(
        entity = OrderDraftEntity::class,
        parentColumns = ["id"],
        childColumns = ["orderId"],
        onDelete = ForeignKey.RESTRICT,
    )],
    indices = [Index("orderId"), Index("productId")],
)
data class OrderDraftItemEntity(
    val orderId: String,
    val productId: String,
    val productSku: String,
    val productName: String,
    val unitPriceMinor: Long,
    val unitCommissionMinor: Long,
    val quantity: Int,
    val lineTotalMinor: Long,
)
