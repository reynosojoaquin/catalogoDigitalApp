package com.catalogodigital.seller

import android.os.Bundle
import android.widget.ArrayAdapter
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.lifecycle.lifecycleScope
import com.catalogodigital.seller.data.OfflineOrderRepository
import com.catalogodigital.seller.data.OrderDraftPolicy
import com.catalogodigital.seller.data.OrderLineInput
import com.catalogodigital.seller.data.PricedOrderLine
import com.catalogodigital.seller.data.local.CustomerOption
import com.catalogodigital.seller.data.local.ProductEntity
import com.catalogodigital.seller.databinding.ActivityOrderCreateBinding
import com.catalogodigital.seller.security.DeviceIdentity
import com.catalogodigital.seller.sync.SyncScheduler
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.math.BigDecimal
import java.text.NumberFormat

class OrderCreateActivity : ComponentActivity() {
    private lateinit var binding: ActivityOrderCreateBinding
    private lateinit var repository: OfflineOrderRepository
    private var customers = emptyList<CustomerOption>()
    private var products = emptyList<ProductEntity>()
    private val lines = linkedMapOf<String, Pair<ProductEntity, Int>>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityOrderCreateBinding.inflate(layoutInflater)
        setContentView(binding.root)
        repository = OfflineOrderRepository((application as CatalogApplication).database)
        binding.addItem.setOnClickListener { addItem() }
        binding.clearItems.setOnClickListener {
            lines.clear()
            renderLines()
        }
        binding.save.setOnClickListener { save() }
        loadOptions()
    }

    private fun loadOptions() {
        binding.addItem.isEnabled = false
        binding.save.isEnabled = false
        lifecycleScope.launch {
            val loaded = withContext(Dispatchers.IO) {
                repository.availableCustomers() to repository.availableProducts()
            }
            customers = loaded.first
            products = loaded.second
            binding.customer.adapter = ArrayAdapter(
                this@OrderCreateActivity,
                android.R.layout.simple_spinner_dropdown_item,
                customers.map(CustomerOption::fullName),
            )
            binding.product.adapter = ArrayAdapter(
                this@OrderCreateActivity,
                android.R.layout.simple_spinner_dropdown_item,
                products.map { getString(R.string.order_product_format, it.name, formatMoney(it.priceMinor)) },
            )
            val available = customers.isNotEmpty() && products.isNotEmpty()
            binding.addItem.isEnabled = available
            binding.save.isEnabled = available
            if (!available) Toast.makeText(this@OrderCreateActivity, R.string.order_catalog_empty, Toast.LENGTH_LONG).show()
            renderLines()
        }
    }

    private fun addItem() {
        val product = products.getOrNull(binding.product.selectedItemPosition)
        val quantity = binding.quantity.text?.toString()?.toIntOrNull()
        if (product == null || quantity == null || quantity <= 0) {
            Toast.makeText(this, R.string.order_invalid, Toast.LENGTH_LONG).show()
            return
        }
        if (lines.containsKey(product.id)) {
            Toast.makeText(this, R.string.order_product_duplicate, Toast.LENGTH_LONG).show()
            return
        }
        try {
            val prospective = lines.values.map { (existingProduct, existingQuantity) ->
                pricedLine(existingProduct, existingQuantity)
            } + pricedLine(product, quantity)
            OrderDraftPolicy.total(prospective)
        } catch (_: ArithmeticException) {
            Toast.makeText(this, R.string.order_invalid, Toast.LENGTH_LONG).show()
            return
        }
        lines[product.id] = product to quantity
        binding.quantity.text?.clear()
        renderLines()
    }

    private fun renderLines() {
        binding.items.text = lines.values.joinToString("\n") { (product, quantity) ->
            getString(
                R.string.order_line_format,
                product.name,
                quantity,
                formatMoney(Math.multiplyExact(product.priceMinor, quantity.toLong())),
            )
        }
        val priced = lines.values.map { (product, quantity) -> pricedLine(product, quantity) }
        val total = OrderDraftPolicy.total(priced)
        binding.total.text = getString(R.string.order_total_format, formatMoney(total))
    }

    private fun save() {
        val customer = customers.getOrNull(binding.customer.selectedItemPosition)
        val inputs = lines.values.map { (product, quantity) -> OrderLineInput(product.id, quantity) }
        if (customer == null || inputs.isEmpty()) {
            Toast.makeText(this, R.string.order_invalid, Toast.LENGTH_LONG).show()
            return
        }
        binding.save.isEnabled = false
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    repository.create(DeviceIdentity(this@OrderCreateActivity).id(), customer.id, inputs)
                }
                Toast.makeText(this@OrderCreateActivity, R.string.order_saved, Toast.LENGTH_LONG).show()
                SyncScheduler.runNow(this@OrderCreateActivity)
                finish()
            } catch (error: Exception) {
                if (error is CancellationException) throw error
                val message = if (error is IllegalArgumentException || error is ArithmeticException) {
                    R.string.order_invalid
                } else {
                    R.string.order_save_failed
                }
                Toast.makeText(this@OrderCreateActivity, message, Toast.LENGTH_LONG).show()
                binding.save.isEnabled = true
            }
        }
    }

    private fun formatMoney(minor: Long): String = NumberFormat.getCurrencyInstance().format(
        BigDecimal.valueOf(minor).movePointLeft(2),
    )

    private fun pricedLine(product: ProductEntity, quantity: Int) = PricedOrderLine(
        product.id, product.sku, product.name, product.priceMinor,
        product.commissionMinor, quantity,
    )
}
