package com.catalogodigital.seller.security

import android.content.Context
import android.util.Base64

class SessionStore(context: Context, private val cipher: KeystoreCipher = KeystoreCipher()) {
    private val preferences = context.getSharedPreferences("secure_session", Context.MODE_PRIVATE)

    fun save(token: String, userId: String) {
        val encryptedToken = cipher.encrypt(token.encodeToByteArray())
        val encryptedUserId = cipher.encrypt(userId.encodeToByteArray())
        preferences.edit()
            .putString(TOKEN, encode(encryptedToken.ciphertext))
            .putString(TOKEN_IV, encode(encryptedToken.iv))
            .putString(USER_ID, encode(encryptedUserId.ciphertext))
            .putString(USER_ID_IV, encode(encryptedUserId.iv))
            .apply()
    }

    fun token(): String? = read(TOKEN, TOKEN_IV)

    fun userId(): String? = read(USER_ID, USER_ID_IV)

    fun hasCompleteSession(): Boolean = !token().isNullOrBlank() && !userId().isNullOrBlank()

    fun clearToken() = preferences.edit().remove(TOKEN).remove(TOKEN_IV).apply()

    fun clear() = preferences.edit().clear().apply()

    private fun read(valueKey: String, ivKey: String): String? = try {
        val ciphertext = preferences.getString(valueKey, null) ?: return null
        val iv = preferences.getString(ivKey, null) ?: return null
        cipher.decrypt(EncryptedValue(decode(ciphertext), decode(iv))).decodeToString()
    } catch (_: RuntimeException) {
        null
    }

    private fun encode(value: ByteArray): String = Base64.encodeToString(value, Base64.NO_WRAP)
    private fun decode(value: String): ByteArray = Base64.decode(value, Base64.NO_WRAP)

    private companion object {
        const val TOKEN = "token_ciphertext"
        const val TOKEN_IV = "token_iv"
        const val USER_ID = "user_id_ciphertext"
        const val USER_ID_IV = "user_id_iv"
    }
}
