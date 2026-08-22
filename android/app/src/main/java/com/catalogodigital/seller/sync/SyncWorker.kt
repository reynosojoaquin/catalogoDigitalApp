package com.catalogodigital.seller.sync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.catalogodigital.seller.BuildConfig
import com.catalogodigital.seller.CatalogApplication
import com.catalogodigital.seller.data.OperationQueue
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.security.SessionStore
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class SyncWorker(context: Context, parameters: WorkerParameters) : CoroutineWorker(context, parameters) {
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val dao = (applicationContext as CatalogApplication).database.pendingOperationDao()
        dao.recoverInterrupted(OperationStatus.IN_FLIGHT, OperationStatus.PENDING)
        val operations = dao.claim(BATCH_SIZE, System.currentTimeMillis())
        if (operations.isEmpty()) return@withContext Result.success()

        val token = SessionStore(applicationContext).token()
        if (BuildConfig.API_BASE_URL.isBlank() || token.isNullOrBlank()) {
            operations.forEach { dao.updateResult(it.operationId, OperationStatus.PENDING, null) }
            return@withContext Result.failure()
        }

        try {
            val queue = OperationQueue(dao)
            val results = SyncApiClient(BuildConfig.API_BASE_URL, token).push(operations, queue)
            results.forEach { dao.updateResult(it.operationId, it.status, it.conflictCode) }
            if (operations.size == BATCH_SIZE) Result.retry() else Result.success()
        } catch (_: Exception) {
            operations.forEach { dao.updateResult(it.operationId, OperationStatus.PENDING, null) }
            Result.retry()
        }
    }

    private companion object {
        const val BATCH_SIZE = 50
    }
}
