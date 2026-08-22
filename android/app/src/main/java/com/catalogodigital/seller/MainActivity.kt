package com.catalogodigital.seller

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.local.OperationStatus
import com.catalogodigital.seller.databinding.ActivityMainBinding
import com.catalogodigital.seller.sync.SyncScheduler
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.syncNow.setOnClickListener {
            if (BuildConfig.API_BASE_URL.isBlank()) {
                Toast.makeText(this, R.string.sync_configuration_missing, Toast.LENGTH_LONG).show()
            } else {
                SyncScheduler.runNow(this)
            }
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
}
