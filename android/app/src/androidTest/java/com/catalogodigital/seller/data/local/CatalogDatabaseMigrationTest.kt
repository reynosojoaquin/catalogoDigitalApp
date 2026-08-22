package com.catalogodigital.seller.data.local

import android.content.Context
import androidx.room.testing.MigrationTestHelper
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class CatalogDatabaseMigrationTest {
    private val context = ApplicationProvider.getApplicationContext<Context>()
    private val databaseName = "catalog-migration-test"

    @get:Rule
    val helper = MigrationTestHelper(
        InstrumentationRegistry.getInstrumentation(),
        CatalogDatabase::class.java,
    )

    @After
    fun removeDatabase() {
        context.deleteDatabase(databaseName)
    }

    @Test
    fun migrateFromVersionOneToEightPreservesQueuedOperation() {
        helper.createDatabase(databaseName, 1).apply {
            execSQL(
                """
                INSERT INTO pending_operations (
                    operationId, operationType, idempotencyKey, deviceId, clientTimestamp,
                    clientVersion, encryptedPayload, payloadIv, status, attemptCount,
                    lastAttemptAtEpochMillis, conflictCode
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """.trimIndent(),
                arrayOf(
                    "operation-1", "customer_create", "idempotency-1", "device-1",
                    "2026-01-01T00:00:00Z", 1L, byteArrayOf(1), byteArrayOf(2),
                    OperationStatus.PENDING, 0, null, null,
                ),
            )
            close()
        }

        val migrated = helper.runMigrationsAndValidate(
            databaseName,
            8,
            true,
            *CatalogDatabase.ALL_MIGRATIONS,
        )

        migrated.query(
            "SELECT operationType, status, entityId FROM pending_operations WHERE operationId = ?",
            arrayOf("operation-1"),
        ).use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals("customer_create", cursor.getString(0))
            assertEquals(OperationStatus.PENDING, cursor.getString(1))
            assertTrue(cursor.isNull(2))
        }
        migrated.query("SELECT COUNT(*) FROM return_drafts").use { cursor ->
            assertTrue(cursor.moveToFirst())
            assertEquals(0, cursor.getInt(0))
        }
        migrated.close()
    }
}
