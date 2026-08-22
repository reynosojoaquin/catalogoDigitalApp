package com.catalogodigital.seller.sync

import com.catalogodigital.seller.data.OperationQueue
import com.catalogodigital.seller.data.local.PendingOperation
import com.catalogodigital.seller.network.SecureEndpointPolicy
import org.json.JSONArray
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URI

data class OperationResult(val operationId: String, val status: String, val conflictCode: String?)

class SyncApiClient(private val baseUrl: String, private val token: String) {
    fun push(operations: List<PendingOperation>, queue: OperationQueue): List<OperationResult> {
        SecureEndpointPolicy.requireValid(baseUrl)
        SyncBatchPolicy.requireValid(operations)
        val body = JSONObject().apply {
            put("device_id", operations.first().deviceId)
            put("operations", JSONArray().apply {
                operations.forEach { operation ->
                    put(JSONObject().apply {
                        put("operation_id", operation.operationId)
                        put("operation_type", operation.operationType)
                        put("idempotency_key", operation.idempotencyKey)
                        put("client_timestamp", operation.clientTimestamp)
                        put("client_version", operation.clientVersion)
                        put("payload", JSONObject(queue.decryptPayload(operation)))
                    })
                }
            })
        }
        val endpoint = URI(baseUrl.trimEnd('/') + "/api/sync/batch/").toURL()
        val connection = endpoint.openConnection() as HttpURLConnection
        return try {
            connection.requestMethod = "POST"
            connection.connectTimeout = 15_000
            connection.readTimeout = 30_000
            connection.doOutput = true
            connection.setRequestProperty("Authorization", "Token $token")
            connection.setRequestProperty("Content-Type", "application/json")
            connection.outputStream.use { it.write(body.toString().encodeToByteArray()) }
            if (connection.responseCode !in 200..299) {
                throw SyncTransportException(connection.responseCode)
            }
            val response = connection.inputStream.bufferedReader().use { it.readText() }
            val results = JSONObject(response).getJSONArray("results")
            List(results.length()) { index ->
                val item = results.getJSONObject(index)
                OperationResult(
                    operationId = item.getString("operation_id"),
                    status = item.getString("status"),
                    conflictCode = item.optString("conflict_code").ifBlank { null },
                )
            }
        } finally {
            connection.disconnect()
        }
    }
}

class SyncTransportException(val statusCode: Int) : Exception("Synchronization failed with HTTP $statusCode")
