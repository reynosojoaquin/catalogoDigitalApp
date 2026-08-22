package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

data class ReturnedQuantity(val invoiceItemId: String, val quantity: Long)

@Dao
interface ReturnDraftDao {
    @Insert
    suspend fun insertReturn(draft: ReturnDraftEntity)

    @Insert
    suspend fun insertItems(items: List<ReturnDraftItemEntity>)

    @Query("UPDATE return_drafts SET status = :status WHERE id = :id")
    suspend fun updateStatus(id: String, status: String)

    @Query("""
        SELECT item.invoiceItemId AS invoiceItemId, SUM(item.quantity) AS quantity
        FROM return_draft_items AS item
        INNER JOIN return_drafts AS draft ON draft.id = item.returnId
        WHERE draft.status NOT IN ('conflict', 'rejected')
          AND NOT EXISTS (
            SELECT 1 FROM business_documents AS document
            WHERE document.entityType = 'return' AND document.entityId = draft.id
          )
        GROUP BY item.invoiceItemId
    """)
    suspend fun returnedQuantities(): List<ReturnedQuantity>
}
