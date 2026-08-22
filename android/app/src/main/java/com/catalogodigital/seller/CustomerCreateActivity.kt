package com.catalogodigital.seller

import android.os.Bundle
import android.view.WindowManager
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.DuplicateLocalCustomerException
import com.catalogodigital.seller.data.OfflineCustomerRepository
import com.catalogodigital.seller.databinding.ActivityCustomerCreateBinding
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.sync.SyncScheduler
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class CustomerCreateActivity : ComponentActivity() {
    private lateinit var binding: ActivityCustomerCreateBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        binding = ActivityCustomerCreateBinding.inflate(layoutInflater)
        setContentView(binding.root)
        binding.save.setOnClickListener { save() }
    }

    private fun save() {
        val fullName = binding.fullName.text?.toString().orEmpty()
        val email = binding.email.text?.toString()
        val phone = binding.phone.text?.toString()
        val identity = binding.identity.text?.toString()
        binding.identity.text?.clear()
        binding.save.isEnabled = false
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    OfflineCustomerRepository((application as CatalogApplication).database).create(
                        deviceId = DeviceIdentity(this@CustomerCreateActivity).id(),
                        fullName = fullName,
                        email = email,
                        phone = phone,
                        identity = identity,
                    )
                }
                Toast.makeText(this@CustomerCreateActivity, R.string.customer_saved, Toast.LENGTH_LONG).show()
                SyncScheduler.runNow(this@CustomerCreateActivity)
                finish()
            } catch (error: Exception) {
                if (error is CancellationException) throw error
                val message = when (error) {
                    is DuplicateLocalCustomerException -> R.string.customer_duplicate
                    is IllegalArgumentException -> R.string.customer_invalid
                    else -> R.string.customer_save_failed
                }
                Toast.makeText(this@CustomerCreateActivity, message, Toast.LENGTH_LONG).show()
                binding.save.isEnabled = true
            }
        }
    }
}
