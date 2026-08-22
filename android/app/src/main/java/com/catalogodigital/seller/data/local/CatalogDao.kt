package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import kotlinx.coroutines.flow.Flow

@Dao
interface CatalogDao {
    @Query("SELECT * FROM customers WHERE isActive = 1 ORDER BY fullName, id")
    fun observeActiveCustomers(): Flow<List<CustomerEntity>>

    @Query("SELECT version FROM customers WHERE id = :id")
    suspend fun customerVersion(id: String): Long?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertCustomer(customer: CustomerEntity)

    @Query("SELECT * FROM products WHERE isActive = 1 ORDER BY name, sku")
    fun observeActiveProducts(): Flow<List<ProductEntity>>

    @Query("SELECT version FROM products WHERE id = :id")
    suspend fun productVersion(id: String): Long?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertProduct(product: ProductEntity)
}
