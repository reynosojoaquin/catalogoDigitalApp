package com.catalogodigital.seller.security

import android.content.Context
import java.util.UUID

class DeviceIdentity(context: Context) {
    private val preferences = context.getSharedPreferences("device_identity", Context.MODE_PRIVATE)

    fun id(): UUID {
        DeviceIdentityPolicy.parseStored(preferences.getString(DEVICE_ID, null))?.let { return it }
        return rotate()
    }

    fun rotate(): UUID = UUID.randomUUID().also {
        preferences.edit().putString(DEVICE_ID, it.toString()).apply()
    }

    private companion object {
        const val DEVICE_ID = "device_id"
    }
}
