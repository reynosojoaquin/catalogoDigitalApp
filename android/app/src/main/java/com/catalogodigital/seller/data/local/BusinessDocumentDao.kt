package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface BusinessDocumentDao {
    @Query("SELECT version FROM business_documents WHERE entityType = :entityType AND entityId = :entityId")
    suspend fun version(entityType: String, entityId: String): Long?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(document: BusinessDocumentEntity)

    @Query("SELECT * FROM business_documents ORDER BY occurredAt DESC, documentKey")
    fun observeAll(): Flow<List<BusinessDocumentEntity>>
}
