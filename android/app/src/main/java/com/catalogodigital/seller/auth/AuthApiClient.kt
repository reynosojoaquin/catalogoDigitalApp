package com.catalogodigital.seller.auth

import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URI

class AuthApiClient(private val baseUrl: String) {
    fun authenticate(username: String, password: CharArray): String {
        val body = JSONObject()
            .put("username", username)
            .put("password", password.concatToString())
        return request("/api/auth/token/", body, null).getString("token")
    }

    fun registerDevice(token: String, deviceId: String, appVersion: String) {
        val body = JSONObject()
            .put("id", deviceId)
            .put("platform", "android")
            .put("app_version", appVersion)
        request("/api/devices/register/", body, token)
    }

    private fun request(path: String, body: JSONObject, token: String?): JSONObject {
        require(baseUrl.startsWith("https://")) { "The API URL must use HTTPS." }
        val connection = URI(baseUrl.trimEnd('/') + path).toURL().openConnection() as HttpURLConnection
        return try {
            connection.requestMethod = "POST"
            connection.connectTimeout = 15_000
            connection.readTimeout = 30_000
            connection.doOutput = true
            connection.setRequestProperty("Content-Type", "application/json")
            if (token != null) connection.setRequestProperty("Authorization", "Token $token")
            connection.outputStream.use { it.write(body.toString().encodeToByteArray()) }
            if (connection.responseCode !in 200..299) throw AuthenticationException(connection.responseCode)
            JSONObject(connection.inputStream.bufferedReader().use { it.readText() })
        } finally {
            connection.disconnect()
        }
    }
}

class AuthenticationException(val statusCode: Int) : Exception("Authentication request failed")
