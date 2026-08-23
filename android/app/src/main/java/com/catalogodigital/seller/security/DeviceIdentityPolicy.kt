package com.catalogodigital.seller.security

import java.util.UUID

object DeviceIdentityPolicy {
    fun parseStored(value: String?): UUID? = value?.let {
        runCatching { UUID.fromString(it) }.getOrNull()
    }
}
