# Android seller application

Base offline-first para vendedores. La cola local conserva cada operación hasta recibir un resultado definitivo del servidor. Los payloads se cifran con una clave AES/GCM no exportable de Android Keystore y WorkManager reintenta solamente cuando existe conectividad.

## Configuración local

Se requiere JDK 17 y Android SDK 35. Define la URL sin incluir `/api` mediante una variable de entorno:

```powershell
$env:CATALOG_API_BASE_URL = "https://your-api-host"
```

También puede definirse `CATALOG_API_BASE_URL` en `android/local.properties`, que está excluido de Git. La aplicación rechaza tráfico HTTP, incluido en desarrollo; el backend local debe publicarse mediante un proxy HTTPS de confianza.

El token de sesión se obtiene del endpoint `/api/auth/token/` y debe entregarse a `SessionStore.saveToken` desde el futuro flujo de inicio de sesión. Se guarda cifrado con Android Keystore; nunca debe incorporarse a BuildConfig, recursos ni archivos versionados.

## Estado de esta fase

- Cola Room durable con UUID, versión, fecha UTC, dispositivo e idempotency key.
- Payload local cifrado y token de sesión cifrado.
- Envío por lotes de hasta 50 operaciones a `/api/sync/batch/`.
- Reintento con restricciones de red y recuperación de trabajo interrumpido.
- Estados internos estables y resumen visible de pendientes, conflictos y rechazos.
- Recursos traducibles en español e inglés, con tema claro, oscuro y automático.

La siguiente fase debe implementar autenticación/registro del dispositivo y las tablas locales de clientes, productos y pedidos antes de conectar las pantallas de captura.
