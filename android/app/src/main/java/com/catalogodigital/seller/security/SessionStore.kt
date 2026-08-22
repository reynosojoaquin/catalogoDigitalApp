package com.catalogodigital.seller.security

import android.content.Context
import android.util.Base64

class SessionStore(context: Context, private val cipher: KeystoreCipher = KeystoreCipher()) {
    private val preferences = context.getSharedPreferences("secure_session", Context.MODE_PRIVATE)

    fun saveToken(token: String) {
        val encrypted = cipher.encrypt(token.encodeToByteArray())
        preferences.edit()
            .putString(TOKEN, Base64.encodeToString(encrypted.ciphertext, Base64.NO_WRAP))
            .putString(TOKEN_IV, Base64.encodeToString(encrypted.iv, Base64.NO_WRAP))
            .apply()
    }

    fun token(): String? {
        val ciphertext = preferences.getString(TOKEN, null) ?: return null
        val iv = preferences.getString(TOKEN_IV, null) ?: return null
        return cipher.decrypt(
            EncryptedValue(
                Base64.decode(ciphertext, Base64.NO_WRAP),
                Base64.decode(iv, Base64.NO_WRAP),
            ),
        ).decodeToString()
    }

    fun clear() = preferences.edit().clear().apply()

    private companion object {
        const val TOKEN = "token_ciphertext"
        const val TOKEN_IV = "token_iv"
    }
}
