package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query

data class CustomerOption(val id: String, val fullName: String)

@Dao
interface OrderDraftDao {
    @Insert
    suspend fun insertOrder(order: OrderDraftEntity)

    @Insert
    suspend fun insertItems(items: List<OrderDraftItemEntity>)

    @Query("SELECT EXISTS(SELECT 1 FROM customers WHERE id = :id AND isActive = 1) OR EXISTS(SELECT 1 FROM customer_drafts WHERE id = :id)")
    suspend fun customerIsAvailable(id: String): Boolean

    @Query("SELECT id, fullName FROM customers WHERE isActive = 1 UNION SELECT id, fullName FROM customer_drafts ORDER BY fullName, id")
    suspend fun availableCustomers(): List<CustomerOption>

    @Query("SELECT * FROM products WHERE isActive = 1 ORDER BY name, sku")
    suspend fun availableProducts(): List<ProductEntity>

    @Query("SELECT * FROM products WHERE id IN (:ids) AND isActive = 1")
    suspend fun activeProductsByIds(ids: List<String>): List<ProductEntity>
}
