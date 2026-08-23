# Catálogo Digital

Plataforma de intermediación comercial con administración web, API central y aplicación Android offline para vendedores.

## Configuración segura

La aplicación obtiene secretos y parámetros sensibles únicamente mediante variables de entorno. Los archivos `*.example` contienen marcadores de configuración y nunca datos reales. No se deben versionar `.env`, `.env.test` ni `.env.production`.

## Desarrollo

1. Copiar `.env.example` como `.env` y reemplazar todos los valores sensibles.
2. Ejecutar `docker compose build`.
3. Ejecutar `docker compose run --rm backend python manage.py migrate`.
4. Ejecutar `docker compose up`.
5. Consultar `http://localhost:8000/health/`.

PostgreSQL y Redis permanecen en una red interna y no publican puertos al host.

## Pruebas

Crear `.env.test` a partir de `.env.test.example` y ejecutar:

```powershell
docker compose -f compose.test.yaml up --build --abort-on-container-exit --exit-code-from backend
docker compose -f compose.test.yaml down --volumes
```

La base de datos de pruebas es efímera y no contiene información de ejemplo en el código de ejecución.

Cada push y pull request ejecuta el workflow de GitHub Actions: valida Compose, prueba el backend con PostgreSQL/Redis, compila Android con lint y ejecuta las pruebas Room en un emulador API 35.

### Android

La URL de la API se configura mediante `CATALOG_API_BASE_URL`; no se incorpora al código fuente. Para verificar la aplicación:

```powershell
cd android
.\gradlew.bat testDebugUnitTest lintDebug assembleDebug assembleDebugAndroidTest
```

Con un emulador o dispositivo conectado, ejecutar además `.\gradlew.bat connectedDebugAndroidTest`. Esta prueba recorre las migraciones Room desde la versión 1 hasta la 8 y comprueba que la cola offline se conserva.

## Producción

1. Crear `.env.production` a partir de `.env.production.example` con secretos aleatorios y el dominio real.
2. Definir `APP_VERSION` con una versión inmutable de la aplicación.
3. Construir la imagen: `docker compose -f compose.production.yaml build backend`.
4. Iniciar servicios: `docker compose -f compose.production.yaml up -d` (el contenedor aplica las migraciones antes de servir tráfico).

Caddy termina TLS automáticamente. El backend no se expone directamente, sirve archivos estáticos con WhiteNoise y valida que depuración esté desactivada y que exista una lista explícita de hosts permitidos.

## Arquitectura

- Backend: Python, Django y Django REST Framework.
- Persistencia: PostgreSQL.
- Coordinación y caché: Redis.
- Aplicación de vendedores: Android con almacenamiento y cola de sincronización offline durables.
- Idioma inicial: `es-DO`; interfaz preparada para internacionalización.
- Zona horaria inicial de presentación: `America/Santo_Domingo`; las fechas se almacenan en UTC.
- La API deniega acceso por defecto; `/health/` es el endpoint público de comprobación.

## Administración web

El dashboard operativo está disponible en `/dashboard/` para usuarios administradores autenticados. Muestra los pendientes de productos, clientes, pedidos, facturas, pagos y devoluciones, además del resumen de comisiones, dispositivos activos y actividad de auditoría. Las vistas propias `/app/catalog/`, `/app/customers/`, `/app/orders/`, `/app/invoices/`, `/app/payments/`, `/app/returns/`, `/app/commissions/` y `/app/audit/` ofrecen tablas con búsqueda, filtros de estado y paginación sobre la base de datos real. No se cargan datos de ejemplo.

El panel `/admin/` permite consultar documentos históricos sin editarlos. Los flujos operativos se ejecutan mediante acciones sobre los registros seleccionados:

- Confirmar entrega completa desde pedidos; la factura interna se genera en la misma transacción.
- Confirmar pagos totales reportados; las comisiones fijas se acreditan automáticamente.
- Confirmar devoluciones; se generan movimientos compensatorios de comisión.
- Liquidar comisiones disponibles desde los perfiles de vendedores.

Estas acciones solo están disponibles para superusuarios o personal con rol administrador y el permiso Django correspondiente. Todas reutilizan los servicios de dominio, generan claves de idempotencia y producen eventos de auditoría.

## Protección de autenticación

Los intentos de inicio de sesión se limitan mediante Redis y se auditan sin almacenar credenciales. `AUTH_LOGIN_RATE` define la tasa por IP y `TRUSTED_PROXY_COUNT` indica cuántos proxies controlados existen delante de Django. En la composición de producción el único proxy confiable es Caddy.

Los feeds de catálogo y operaciones exigen el UUID de un dispositivo activo perteneciente al vendedor. Al revocar un dispositivo desde la administración, este deja de descargar información y la aplicación elimina la sesión local al recibir la denegación.

Android cifra por separado el token y el identificador estable del vendedor. Las pantallas comerciales requieren una sesión local completa. Un cambio de cuenta nunca reutiliza el caché anterior y se bloquea mientras existan operaciones pendientes, rechazadas o en conflicto, evitando pérdida o exposición cruzada de datos offline.

Consulta [AGENTS.md](AGENTS.md) para las reglas funcionales y técnicas del proyecto.
