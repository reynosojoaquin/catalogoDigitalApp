package com.catalogodigital.seller

import android.content.Intent
import androidx.activity.ComponentActivity
import com.catalogodigital.seller.security.SessionStore

abstract class AuthenticatedActivity : ComponentActivity() {
    override fun onStart() {
        super.onStart()
        if (!SessionStore(this).hasCompleteSession()) {
            startActivity(
                Intent(this, MainActivity::class.java).addFlags(
                    Intent.FLAG_ACTIVITY_CLEAR_TOP or Intent.FLAG_ACTIVITY_SINGLE_TOP,
                ),
            )
            finish()
        }
    }
}
