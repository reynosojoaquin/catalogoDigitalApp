package com.catalogodigital.seller.sync

import com.catalogodigital.seller.network.SecureEndpointPolicy
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URI

class BusinessFeedApiClient(private val baseUrl: String, private val token: String) {
    fun changes(after: Long): BusinessFeedPage {
        SecureEndpointPolicy.requireValid(baseUrl)
        val endpoint = URI(
            baseUrl.trimEnd('/') + "/api/sync/business-changes/?after=$after&limit=$PAGE_SIZE",
        ).toURL()
        val connection = endpoint.openConnection() as HttpURLConnection
        return try {
            connection.requestMethod = "GET"
            connection.connectTimeout = 15_000
            connection.readTimeout = 30_000
            connection.setRequestProperty("Authorization", "Token $token")
            connection.setRequestProperty("Accept", "application/json")
            if (connection.responseCode !in 200..299) throw SyncTransportException(connection.responseCode)
            parse(JSONObject(connection.inputStream.bufferedReader().use { it.readText() }))
        } finally {
            connection.disconnect()
        }
    }

    private fun parse(response: JSONObject): BusinessFeedPage {
        val items = response.getJSONArray("changes")
        return BusinessFeedPage(
            changes = List(items.length()) { index ->
                val item = items.getJSONObject(index)
                val data = item.optJSONObject("data")
                    ?: throw IllegalArgumentException("A business change must contain entity data.")
                BusinessFeedChange(
                    sequence = item.getLong("sequence"),
                    entityType = item.getString("entity_type"),
                    entityId = item.getString("entity_id"),
                    version = item.getLong("version"),
                    occurredAt = item.getString("occurred_at"),
                    dataId = data.getString("id"),
                    dataVersion = if (data.has("version") && !data.isNull("version")) data.getLong("version") else null,
                    dataJson = data.toString(),
                )
            },
            nextCursor = response.getLong("next_cursor"),
            hasMore = response.getBoolean("has_more"),
        )
    }

    private companion object {
        const val PAGE_SIZE = 200
    }
}
