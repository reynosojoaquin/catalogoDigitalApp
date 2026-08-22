package com.catalogodigital.seller.data.local

import androidx.room.Entity
import androidx.room.Index
import androidx.room.PrimaryKey

object OperationStatus {
    const val PENDING = "pending"
    const val IN_FLIGHT = "in_flight"
    const val APPLIED = "applied"
    const val CONFLICT = "conflict"
    const val REJECTED = "rejected"
}

@Entity(
    tableName = "pending_operations",
    indices = [Index("status"), Index(value = ["idempotencyKey"], unique = true)],
)
data class PendingOperation(
    @PrimaryKey val operationId: String,
    val operationType: String,
    val idempotencyKey: String,
    val deviceId: String,
    val clientTimestamp: String,
    val clientVersion: Long,
    val encryptedPayload: ByteArray,
    val payloadIv: ByteArray,
    val status: String = OperationStatus.PENDING,
    val attemptCount: Int = 0,
    val lastAttemptAtEpochMillis: Long? = null,
    val conflictCode: String? = null,
)
