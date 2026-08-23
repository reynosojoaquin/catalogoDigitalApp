# Android seller application

Aplicación offline-first para vendedores. La cola Room conserva cada operación hasta recibir un resultado definitivo del servidor. Los payloads y la sesión se cifran con Android Keystore; WorkManager reintenta únicamente cuando existe conectividad.

## Configuración local

Se requiere JDK 17 y Android SDK 35. Define la URL de la API sin incluir `/api` mediante una variable de entorno:

```powershell
$env:CATALOG_API_BASE_URL = "https://your-api-host"
```

También puede definirse `CATALOG_API_BASE_URL` en `android/local.properties`, que está excluido de Git. La aplicación rechaza tráfico HTTP. Nunca se incorporan credenciales a BuildConfig, recursos ni archivos versionados.

## Capacidades verificadas

- Cola Room durable con UUID, versión, fecha UTC, dispositivo e idempotency key.
- Payload, token e identidad del vendedor cifrados.
- Envío por lotes y recuperación de trabajo interrumpido.
- Estados visibles de pendientes, conflictos y rechazos.
- Protección de feeds mediante dispositivo activo.
- Aislamiento de sesión y bloqueo de cambio de cuenta con operaciones no resueltas.
- Recursos traducibles en español e inglés, con tema claro, oscuro y automático.
- Migraciones Room verificadas desde la versión 1 hasta la 8.

## Pruebas

```powershell
.\gradlew.bat testDebugUnitTest lintDebug assembleDebug assembleDebugAndroidTest
```

Con un emulador o dispositivo conectado, ejecutar además:

```powershell
.\gradlew.bat connectedDebugAndroidTest
```

## Artefactos release

Las compilaciones de distribución reciben `ANDROID_VERSION_CODE` y `ANDROID_VERSION_NAME` desde el entorno. La firma se activa cuando se proporcionan `ANDROID_KEYSTORE_PATH`, `ANDROID_KEYSTORE_PASSWORD`, `ANDROID_KEY_ALIAS` y `ANDROID_KEY_PASSWORD`; el keystore debe existir fuera del repositorio.

```powershell
$env:CATALOG_API_BASE_URL = "https://your-api-host"
$env:ANDROID_VERSION_CODE = "1"
$env:ANDROID_VERSION_NAME = "0.1.0"
$env:ANDROID_KEYSTORE_PATH = "C:\secure\catalogo-release.jks"
$env:ANDROID_KEYSTORE_PASSWORD = "<provided-outside-repository>"
$env:ANDROID_KEY_ALIAS = "<provided-outside-repository>"
$env:ANDROID_KEY_PASSWORD = "<provided-outside-repository>"
.\gradlew.bat bundleRelease
```

No se deben guardar esos valores en `local.properties`, código, recursos ni archivos versionados.
