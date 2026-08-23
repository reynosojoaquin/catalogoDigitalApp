package com.catalogodigital.seller

import android.os.Bundle
import android.content.Intent
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.result.contract.ActivityResultContracts
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.databinding.ActivityMainBinding
import com.catalogodigital.seller.sync.SyncScheduler
import com.catalogodigital.seller.security.SessionStore
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private lateinit var binding: ActivityMainBinding
    private var loginInProgress = false
    private val login = registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
        loginInProgress = false
        if (result.resultCode == RESULT_OK) SyncScheduler.runNow(this) else finish()
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.createCustomer.setOnClickListener {
            startActivity(Intent(this, CustomerCreateActivity::class.java))
        }
        binding.createOrder.setOnClickListener {
            startActivity(Intent(this, OrderCreateActivity::class.java))
        }
        binding.viewOperations.setOnClickListener {
            startActivity(Intent(this, BusinessDocumentsActivity::class.java))
        }
        binding.createPayment.setOnClickListener {
            startActivity(Intent(this, PaymentCreateActivity::class.java))
        }
        binding.createReturn.setOnClickListener {
            startActivity(Intent(this, ReturnCreateActivity::class.java))
        }
        binding.viewSyncIssues.setOnClickListener {
            startActivity(Intent(this, SyncIssuesActivity::class.java))
        }

        binding.syncNow.setOnClickListener {
            if (BuildConfig.API_BASE_URL.isBlank()) {
                Toast.makeText(this, R.string.sync_configuration_missing, Toast.LENGTH_LONG).show()
            } else {
                SyncScheduler.runNow(this)
            }
        }
        binding.logout.setOnClickListener {
            SessionStore(this).clearToken()
            requireSession()
        }

        val dao = (application as CatalogApplication).database.pendingOperationDao()
        lifecycleScope.launch {
            dao.observeStatusCounts().collect { counts ->
                val indexed = counts.associate { it.status to it.count }
                binding.pendingCount.text = getString(R.string.sync_pending, indexed[OperationStatus.PENDING] ?: 0)
                binding.conflictCount.text = getString(R.string.sync_conflicts, indexed[OperationStatus.CONFLICT] ?: 0)
                binding.rejectedCount.text = getString(R.string.sync_rejected, indexed[OperationStatus.REJECTED] ?: 0)
            }
        }
    }

    override fun onResume() {
        super.onResume()
        requireSession()
    }

    private fun requireSession() {
        if (isFinishing || isDestroyed) return
        if (!SessionStore(this).hasCompleteSession() && !loginInProgress) {
            loginInProgress = true
            login.launch(Intent(this, LoginActivity::class.java))
        }
    }
}
