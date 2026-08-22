package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

@Dao
interface CustomerDraftDao {
    @Insert
    suspend fun insert(draft: CustomerDraftEntity)

    @Query("SELECT COUNT(*) FROM customer_drafts WHERE email = :email")
    suspend fun countByEmail(email: String): Int

    @Query("SELECT COUNT(*) FROM customer_drafts WHERE phone = :phone")
    suspend fun countByPhone(phone: String): Int

    @Query("SELECT COUNT(*) FROM customer_drafts WHERE identityFingerprint = :fingerprint")
    suspend fun countByIdentity(fingerprint: ByteArray): Int

    @Query("DELETE FROM customer_drafts WHERE id = :id")
    suspend fun deleteById(id: String)
}
