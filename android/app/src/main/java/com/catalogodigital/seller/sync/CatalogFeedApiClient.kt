package com.catalogodigital.seller.sync

import com.catalogodigital.seller.network.SecureEndpointPolicy
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URI

class CatalogFeedApiClient(private val baseUrl: String, private val token: String) {
    fun changes(after: Long): CatalogFeedPage {
        val response = request("/api/sync/catalog-changes/?after=$after&limit=$PAGE_SIZE", "GET")
        val items = response.getJSONArray("changes")
        return CatalogFeedPage(
            changes = List(items.length()) { index -> parseChange(items.getJSONObject(index)) },
            nextCursor = response.getLong("next_cursor"),
            hasMore = response.getBoolean("has_more"),
        )
    }

    fun acknowledge(deviceId: String, sequence: Long) {
        val body = JSONObject().put("device_id", deviceId).put("sequence", sequence)
        request("/api/sync/cursor/ack/", "POST", body)
    }

    private fun parseChange(change: JSONObject): CatalogFeedChange {
        val dataObject = change.optJSONObject("data")
            ?: throw IllegalArgumentException("A catalog change must contain entity data.")
        val data = buildMap<String, Any?> {
            dataObject.keys().forEach { key ->
                put(key, if (dataObject.isNull(key)) null else dataObject.get(key))
            }
        }
        return CatalogFeedChange(
            sequence = change.getLong("sequence"),
            entityType = change.getString("entity_type"),
            entityId = change.getString("entity_id"),
            version = change.getLong("version"),
            data = data,
        )
    }

    private fun request(path: String, method: String, body: JSONObject? = null): JSONObject {
        SecureEndpointPolicy.requireValid(baseUrl)
        val connection = URI(baseUrl.trimEnd('/') + path).toURL().openConnection() as HttpURLConnection
        return try {
            connection.requestMethod = method
            connection.connectTimeout = 15_000
            connection.readTimeout = 30_000
            connection.setRequestProperty("Authorization", "Token $token")
            connection.setRequestProperty("Accept", "application/json")
            if (body != null) {
                connection.doOutput = true
                connection.setRequestProperty("Content-Type", "application/json")
                connection.outputStream.use { it.write(body.toString().encodeToByteArray()) }
            }
            if (connection.responseCode !in 200..299) throw SyncTransportException(connection.responseCode)
            JSONObject(connection.inputStream.bufferedReader().use { it.readText() })
        } finally {
            connection.disconnect()
        }
    }

    private companion object {
        const val PAGE_SIZE = 200
    }
}
