package com.catalogodigital.seller

import android.app.Activity
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.auth.AuthApiClient
import com.catalogodigital.seller.databinding.ActivityLoginBinding
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.security.SessionStore
import com.catalogodigital.seller.security.SessionSwitchAction
import com.catalogodigital.seller.security.SessionSwitchPolicy
import com.catalogodigital.seller.data.local.OperationStatus
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class LoginActivity : ComponentActivity() {
    private lateinit var binding: ActivityLoginBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.login.setOnClickListener { login() }
    }

    private fun login() {
        val username = binding.username.text?.toString()?.trim().orEmpty()
        val password = binding.password.text?.toString()?.toCharArray() ?: CharArray(0)
        if (username.isBlank() || password.isEmpty() || BuildConfig.API_BASE_URL.isBlank()) {
            password.fill('\u0000')
            showFailure()
            return
        }
        binding.login.isEnabled = false
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    val client = AuthApiClient(BuildConfig.API_BASE_URL)
                    val session = client.authenticate(username, password)
                    val store = SessionStore(this@LoginActivity)
                    val database = (application as CatalogApplication).database
                    val unresolved = database.pendingOperationDao().countByStatuses(
                        listOf(
                            OperationStatus.PENDING,
                            OperationStatus.IN_FLIGHT,
                            OperationStatus.CONFLICT,
                            OperationStatus.REJECTED,
                        ),
                    )
                    val deviceIdentity = DeviceIdentity(this@LoginActivity)
                    when (SessionSwitchPolicy.action(store.userId(), session.userId, unresolved)) {
                        SessionSwitchAction.KEEP_DATA -> Unit
                        SessionSwitchAction.CLEAR_DATA -> {
                            database.clearAllTables()
                            deviceIdentity.rotate()
                        }
                        SessionSwitchAction.BLOCK -> throw AccountSwitchBlockedException()
                    }
                    client.registerDevice(
                        session.token,
                        deviceIdentity.id().toString(),
                        BuildConfig.VERSION_NAME,
                    )
                    store.save(session.token, session.userId)
                }
                setResult(Activity.RESULT_OK)
                finish()
            } catch (_: AccountSwitchBlockedException) {
                Toast.makeText(this@LoginActivity, R.string.login_account_switch_blocked, Toast.LENGTH_LONG).show()
            } catch (error: Exception) {
                if (error is CancellationException) throw error
                showFailure()
            } finally {
                password.fill('\u0000')
                binding.password.text?.clear()
                binding.login.isEnabled = true
            }
        }
    }

    private fun showFailure() = Toast.makeText(this, R.string.login_failed, Toast.LENGTH_LONG).show()
}

private class AccountSwitchBlockedException : Exception()
