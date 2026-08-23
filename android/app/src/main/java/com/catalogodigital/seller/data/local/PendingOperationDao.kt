package com.catalogodigital.seller.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Transaction
import kotlinx.coroutines.flow.Flow

data class StatusCount(val status: String, val count: Int)

@Dao
interface PendingOperationDao {
    @Insert
    suspend fun insert(operation: PendingOperation)

    @Query("SELECT status, COUNT(*) AS count FROM pending_operations GROUP BY status")
    fun observeStatusCounts(): Flow<List<StatusCount>>

    @Query("SELECT * FROM pending_operations WHERE status IN (:statuses) ORDER BY clientTimestamp DESC")
    fun observeIssues(statuses: List<String>): Flow<List<PendingOperation>>

    @Query("SELECT COUNT(*) FROM pending_operations WHERE status IN (:statuses)")
    suspend fun countByStatuses(statuses: List<String>): Int

    @Query("SELECT * FROM pending_operations WHERE status = :status ORDER BY clientTimestamp LIMIT :limit")
    suspend fun findByStatus(status: String, limit: Int): List<PendingOperation>

    @Query("UPDATE pending_operations SET status = :newStatus, attemptCount = attemptCount + 1, lastAttemptAtEpochMillis = :attemptedAt WHERE operationId IN (:ids) AND status = :expectedStatus")
    suspend fun updateForAttempt(ids: List<String>, expectedStatus: String, newStatus: String, attemptedAt: Long): Int

    @Query("UPDATE pending_operations SET status = :status, conflictCode = :conflictCode WHERE operationId = :operationId")
    suspend fun updateResult(operationId: String, status: String, conflictCode: String?)

    @Query("UPDATE pending_operations SET status = :pendingStatus WHERE status = :inFlightStatus")
    suspend fun recoverInterrupted(inFlightStatus: String, pendingStatus: String)

    @Transaction
    suspend fun claim(limit: Int, attemptedAt: Long): List<PendingOperation> {
        val candidates = findByStatus(OperationStatus.PENDING, limit)
        if (candidates.isEmpty()) return emptyList()
        val changed = updateForAttempt(
            candidates.map(PendingOperation::operationId),
            OperationStatus.PENDING,
            OperationStatus.IN_FLIGHT,
            attemptedAt,
        )
        return if (changed == candidates.size) candidates else emptyList()
    }
}
