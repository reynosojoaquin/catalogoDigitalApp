package com.catalogodigital.seller

import android.os.Bundle
import android.view.View
import android.widget.AdapterView
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.OfflineReturnRepository
import com.catalogodigital.seller.data.ReturnDraftPolicy
import com.catalogodigital.seller.data.ReturnLineInput
import com.catalogodigital.seller.data.ReturnableInvoice
import com.catalogodigital.seller.data.ReturnableInvoiceItem
import com.catalogodigital.seller.databinding.ActivityReturnCreateBinding
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.sync.SyncScheduler
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.math.BigDecimal
import java.text.NumberFormat

class ReturnCreateActivity : ComponentActivity() {
    private lateinit var binding: ActivityReturnCreateBinding
    private lateinit var repository: OfflineReturnRepository
    private var invoices = emptyList<ReturnableInvoice>()
    private val lines = linkedMapOf<String, Pair<ReturnableInvoiceItem, Int>>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityReturnCreateBinding.inflate(layoutInflater)
        setContentView(binding.root)
        repository = OfflineReturnRepository((application as CatalogApplication).database)
        binding.invoice.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                lines.clear()
                updateItemOptions()
                renderLines()
            }
            override fun onNothingSelected(parent: AdapterView<*>?) = Unit
        }
        binding.addItem.setOnClickListener { addItem() }
        binding.clearItems.setOnClickListener {
            lines.clear()
            renderLines()
        }
        binding.save.setOnClickListener { save() }
        loadInvoices()
    }

    private fun loadInvoices() {
        binding.addItem.isEnabled = false
        binding.save.isEnabled = false
        lifecycleScope.launch {
            invoices = withContext(Dispatchers.IO) { repository.returnableInvoices() }
            binding.invoice.adapter = ArrayAdapter(
                this@ReturnCreateActivity,
                android.R.layout.simple_spinner_dropdown_item,
                invoices.map(ReturnableInvoice::label),
            )
            updateItemOptions()
            val available = invoices.isNotEmpty()
            binding.addItem.isEnabled = available
            binding.save.isEnabled = available
            if (!available) Toast.makeText(this@ReturnCreateActivity, R.string.return_no_invoices, Toast.LENGTH_LONG).show()
            renderLines()
        }
    }

    private fun updateItemOptions() {
        val items = currentInvoice()?.items.orEmpty()
        binding.item.adapter = ArrayAdapter(
            this,
            android.R.layout.simple_spinner_dropdown_item,
            items.map { getString(R.string.return_item_format, it.productName, it.availableQuantity) },
        )
    }

    private fun addItem() {
        val item = currentInvoice()?.items?.getOrNull(binding.item.selectedItemPosition)
        val quantity = binding.quantity.text?.toString()?.toIntOrNull()
        if (item == null || quantity == null || quantity <= 0 || quantity > item.availableQuantity) {
            Toast.makeText(this, R.string.return_invalid, Toast.LENGTH_LONG).show()
            return
        }
        if (lines.containsKey(item.invoiceItemId)) {
            Toast.makeText(this, R.string.return_duplicate, Toast.LENGTH_LONG).show()
            return
        }
        try {
            val prospective = lines.values.map { (existing, existingQuantity) ->
                ReturnLineInput(existing.invoiceItemId, existingQuantity)
            } + ReturnLineInput(item.invoiceItemId, quantity)
            val available = (lines.values.map { it.first } + item)
                .associateBy(ReturnableInvoiceItem::invoiceItemId)
            ReturnDraftPolicy.validate(prospective, available)
            ReturnDraftPolicy.total(prospective, available)
            ReturnDraftPolicy.commissionTotal(prospective, available)
        } catch (_: ArithmeticException) {
            Toast.makeText(this, R.string.return_invalid, Toast.LENGTH_LONG).show()
            return
        }
        lines[item.invoiceItemId] = item to quantity
        binding.quantity.text?.clear()
        renderLines()
    }

    private fun renderLines() {
        binding.items.text = lines.values.joinToString("\n") { (item, quantity) ->
            getString(
                R.string.return_line_format,
                item.productName,
                quantity,
                formatMoney(Math.multiplyExact(item.unitPriceMinor, quantity.toLong())),
            )
        }
        val inputs = lines.values.map { (item, quantity) -> ReturnLineInput(item.invoiceItemId, quantity) }
        val available = lines.values.associate { (item, _quantity) -> item.invoiceItemId to item }
        binding.total.text = getString(
            R.string.return_total_format,
            formatMoney(ReturnDraftPolicy.total(inputs, available)),
        )
    }

    private fun save() {
        val invoice = currentInvoice()
        val inputs = lines.values.map { (item, quantity) -> ReturnLineInput(item.invoiceItemId, quantity) }
        if (invoice == null || inputs.isEmpty()) {
            Toast.makeText(this, R.string.return_invalid, Toast.LENGTH_LONG).show()
            return
        }
        binding.save.isEnabled = false
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    repository.create(DeviceIdentity(this@ReturnCreateActivity).id(), invoice.id, inputs)
                }
                Toast.makeText(this@ReturnCreateActivity, R.string.return_saved, Toast.LENGTH_LONG).show()
                SyncScheduler.runNow(this@ReturnCreateActivity)
                finish()
            } catch (error: Exception) {
                if (error is CancellationException) throw error
                val message = if (error is IllegalArgumentException || error is ArithmeticException) {
                    R.string.return_invalid
                } else {
                    R.string.return_save_failed
                }
                Toast.makeText(this@ReturnCreateActivity, message, Toast.LENGTH_LONG).show()
                binding.save.isEnabled = true
            }
        }
    }

    private fun currentInvoice(): ReturnableInvoice? = invoices.getOrNull(binding.invoice.selectedItemPosition)

    private fun formatMoney(minor: Long): String = NumberFormat.getCurrencyInstance().format(
        BigDecimal.valueOf(minor).movePointLeft(2),
    )
}
