package com.catalogodigital.seller

import android.app.Application
import com.catalogodigital.seller.data.local.CatalogDatabase
import com.catalogodigital.seller.sync.SyncScheduler

class CatalogApplication : Application() {
    val database by lazy { CatalogDatabase.create(this) }

    override fun onCreate() {
        super.onCreate()
        SyncScheduler.schedulePeriodic(this)
    }
}
