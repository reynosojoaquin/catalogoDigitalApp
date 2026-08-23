package com.catalogodigital.seller.security

enum class SessionSwitchAction { KEEP_DATA, CLEAR_DATA, BLOCK }

object SessionSwitchPolicy {
    fun action(previousUserId: String?, nextUserId: String, unresolvedOperations: Int): SessionSwitchAction {
        require(nextUserId.isNotBlank())
        require(unresolvedOperations >= 0)
        if (previousUserId == nextUserId) return SessionSwitchAction.KEEP_DATA
        return if (unresolvedOperations > 0) SessionSwitchAction.BLOCK else SessionSwitchAction.CLEAR_DATA
    }
}
