package com.catalogodigital.seller

import android.os.Bundle
import android.view.WindowManager
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.OfflinePaymentRepository
import com.catalogodigital.seller.data.PaymentMethod
import com.catalogodigital.seller.data.local.PayableInvoice
import com.catalogodigital.seller.databinding.ActivityPaymentCreateBinding
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.sync.SyncScheduler
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.math.BigDecimal
import java.text.NumberFormat

class PaymentCreateActivity : AuthenticatedActivity() {
    private lateinit var binding: ActivityPaymentCreateBinding
    private lateinit var repository: OfflinePaymentRepository
    private var invoices = emptyList<PayableInvoice>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_SECURE)
        binding = ActivityPaymentCreateBinding.inflate(layoutInflater)
        setContentView(binding.root)
        repository = OfflinePaymentRepository((application as CatalogApplication).database)
        binding.method.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            listOf(getString(R.string.payment_method_cash), getString(R.string.payment_method_terminal)),
        )
        binding.save.setOnClickListener { save() }
        loadInvoices()
    }

    private fun loadInvoices() {
        binding.save.isEnabled = false
        lifecycleScope.launch {
            invoices = withContext(Dispatchers.IO) { repository.payableInvoices() }
            binding.invoice.adapter = ArrayAdapter(
                this@PaymentCreateActivity,
                android.R.layout.simple_spinner_dropdown_item,
                invoices.map { invoice ->
                    getString(
                        R.string.payment_invoice_format,
                        invoice.label ?: invoice.id,
                        formatMoney(invoice.amountMinor),
                    )
                },
            )
            binding.save.isEnabled = invoices.isNotEmpty()
            if (invoices.isEmpty()) {
                Toast.makeText(this@PaymentCreateActivity, R.string.payment_no_invoices, Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun save() {
        val invoice = invoices.getOrNull(binding.invoice.selectedItemPosition) ?: return
        val method = if (binding.method.selectedItemPosition == 0) {
            PaymentMethod.CASH
        } else {
            PaymentMethod.EXTERNAL_CARD_TERMINAL
        }
        val reference = binding.terminalReference.text?.toString()
        binding.terminalReference.text?.clear()
        binding.save.isEnabled = false
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    repository.create(DeviceIdentity(this@PaymentCreateActivity).id(), invoice.id, method, reference)
                }
                Toast.makeText(this@PaymentCreateActivity, R.string.payment_saved, Toast.LENGTH_LONG).show()
                SyncScheduler.runNow(this@PaymentCreateActivity)
                finish()
            } catch (error: Exception) {
                if (error is CancellationException) throw error
                val message = if (error is IllegalArgumentException) {
                    R.string.payment_invalid
                } else {
                    R.string.payment_save_failed
                }
                Toast.makeText(this@PaymentCreateActivity, message, Toast.LENGTH_LONG).show()
                binding.save.isEnabled = true
            }
        }
    }

    private fun formatMoney(minor: Long): String = NumberFormat.getCurrencyInstance().format(
        BigDecimal.valueOf(minor).movePointLeft(2),
    )
}
