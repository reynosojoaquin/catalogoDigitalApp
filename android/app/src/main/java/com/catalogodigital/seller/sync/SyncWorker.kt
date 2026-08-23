package com.catalogodigital.seller.sync

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.catalogodigital.seller.BuildConfig
import com.catalogodigital.seller.CatalogApplication
import com.catalogodigital.seller.data.OperationQueue
import com.catalogodigital.seller.data.CatalogFeedRepository
import com.catalogodigital.seller.data.SyncReconciliationRepository
import com.catalogodigital.seller.data.BusinessFeedRepository
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.security.SessionStore
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.withContext

class SyncWorker(context: Context, parameters: WorkerParameters) : CoroutineWorker(context, parameters) {
    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        val database = (applicationContext as CatalogApplication).database
        val dao = database.pendingOperationDao()
        dao.recoverInterrupted(OperationStatus.IN_FLIGHT, OperationStatus.PENDING)
        val token = SessionStore(applicationContext).token()
        if (BuildConfig.API_BASE_URL.isBlank() || token.isNullOrBlank()) {
            return@withContext Result.failure()
        }

        val operations = dao.claim(SyncBatchPolicy.MAX_OPERATIONS, System.currentTimeMillis())
        try {
            if (operations.isNotEmpty()) {
                val queue = OperationQueue(dao)
                val results = SyncApiClient(BuildConfig.API_BASE_URL, token).push(operations, queue)
                SyncReconciliationRepository(database).apply(operations, results)
            }

            val repository = CatalogFeedRepository(database)
            val feedClient = CatalogFeedApiClient(BuildConfig.API_BASE_URL, token)
            val deviceId = DeviceIdentity(applicationContext).id().toString()
            var catalogHasMore = true
            var pageCount = 0
            while (catalogHasMore && pageCount < MAX_FEED_PAGES) {
                val page = feedClient.changes(repository.cursor(), deviceId)
                repository.apply(page)
                catalogHasMore = page.hasMore
                pageCount += 1
            }

            val businessRepository = BusinessFeedRepository(database)
            val businessClient = BusinessFeedApiClient(BuildConfig.API_BASE_URL, token)
            var businessHasMore = true
            var businessPageCount = 0
            while (businessHasMore && businessPageCount < MAX_FEED_PAGES) {
                val page = businessClient.changes(businessRepository.cursor(), deviceId)
                businessRepository.apply(page)
                businessHasMore = page.hasMore
                businessPageCount += 1
            }
            feedClient.acknowledge(deviceId, maxOf(repository.cursor(), businessRepository.cursor()))
            if (
                operations.size == SyncBatchPolicy.MAX_OPERATIONS ||
                catalogHasMore || businessHasMore
            ) Result.retry() else Result.success()
        } catch (error: Exception) {
            if (error is CancellationException) throw error
            when (
                if (error is SyncTransportException) SyncFailurePolicy.action(error.statusCode)
                else SyncFailureAction.RETRY
            ) {
                SyncFailureAction.AUTHENTICATION_REQUIRED -> {
                    operations.forEach { dao.updateResult(it.operationId, OperationStatus.PENDING, null) }
                    SessionStore(applicationContext).clearToken()
                    Result.failure()
                }
                SyncFailureAction.REJECT_BATCH -> {
                    operations.forEach {
                        dao.updateResult(it.operationId, OperationStatus.REJECTED, "batch_rejected")
                    }
                    Result.failure()
                }
                SyncFailureAction.RETRY -> {
                    operations.forEach { dao.updateResult(it.operationId, OperationStatus.PENDING, null) }
                    Result.retry()
                }
            }
        }
    }

    private companion object {
        const val MAX_FEED_PAGES = 10
    }
}
