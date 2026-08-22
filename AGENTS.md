# AGENTS.md

## Alcance

Estas instrucciones aplican a todo el proyecto `catalogoDigital`.

## Objetivo del proyecto

Desarrollar una plataforma de catálogo digital compuesta por:

- Administración web.
- API central en Python.
- Aplicación Android para vendedores con operación offline.
- Infraestructura reproducible y dockerizada.

El flujo principal es: pedido, entrega completa por la empresa, factura interna, reporte y confirmación del pago total, comisión fija por producto, devolución y liquidación de comisiones.

## Reglas de desarrollo

- No eliminar ni modificar archivos, datos o trabajo existente sin autorización explícita del usuario.
- Antes de tocar un archivo preexistente, inspeccionarlo y confirmar que el cambio está comprendido en la solicitud autorizada.
- Mantener una arquitectura modular y evitar lógica comercial en controladores o vistas.
- Usar nombres técnicos, código y commits en inglés; la documentación funcional puede escribirse en español.
- Incorporar pruebas para reglas de negocio, permisos, sincronización y operaciones financieras.
- Usar `Decimal` para importes monetarios; nunca `float`.
- Guardar fechas en UTC y presentarlas según la región del usuario.
- Mantener los estados internos como códigos estables, nunca como textos traducidos.
- Toda interfaz debe utilizar i18n; no introducir textos visibles directamente cuando puedan traducirse.
- Soportar temas claro, oscuro y automático mediante tokens de diseño.
- Nunca reemplazar trabajo existente para simplificar una implementación.

## Seguridad

- Denegar acceso por defecto y validar permisos en el servidor.
- No guardar secretos, credenciales, tokens ni datos reales en el repositorio.
- No registrar contraseñas, tokens, documentos de identidad ni datos completos de tarjetas.
- La aplicación nunca procesará ni almacenará datos completos de tarjetas; solo referencias de terminal externa.
- Cifrar comunicaciones y proteger documentos de identidad en almacenamiento privado.
- Recalcular precios, totales y comisiones en el servidor.
- Requerir idempotencia para pedidos, pagos, facturas, devoluciones, comisiones y sincronización.
- Auditar autenticación, cambios administrativos y todas las operaciones comerciales o financieras.
- Los eventos de auditoría son de solo anexado y no se editan ni eliminan desde la aplicación.

## Datos y dominio

- No existe control ni reserva de inventario.
- Los precios son centralizados y no se permiten descuentos.
- La factura interna se genera solo después de confirmar una entrega completa.
- Solo se aceptan pagos totales en efectivo o mediante terminal de tarjeta externa.
- La comisión es una cantidad fija por unidad definida en el producto y se acredita al cerrar la factura pagada.
- Los cambios de precio o comisión no alteran documentos históricos.
- Las devoluciones siempre se originan desde una factura y producen movimientos compensatorios, nunca borrados.
- El vendedor puede consultar todos los clientes activos, pero únicamente sus propios pedidos y operaciones asociadas.
- La creación de clientes debe detectar duplicados tanto localmente como al sincronizar.

## Offline y sincronización

- La aplicación Android debe conservar datos y permitir capturas sin conexión, sin límite funcional de tiempo.
- Toda operación offline usa UUID, versión, marca temporal, dispositivo e idempotency key.
- El servidor es la fuente definitiva de precios, permisos, estados y comisiones.
- Nunca resolver conflictos sobrescribiendo datos silenciosamente.
- Conservar una cola durable de sincronización y estados visibles para el vendedor.

## Docker e infraestructura

- Los servicios del servidor deben ejecutarse mediante Docker Compose.
- Los contenedores deben ser reemplazables y no guardar datos persistentes internamente.
- PostgreSQL, Redis y almacenamiento privado no deben exponerse públicamente.
- Ejecutar servicios con usuarios sin privilegios cuando sea posible.
- Mantener configuraciones separadas para desarrollo, pruebas y producción.
- Versionar imágenes y fijar versiones de dependencias.

## Verificación mínima

Antes de entregar cambios:

- Ejecutar las pruebas relacionadas.
- Validar la configuración de Docker Compose.
- Comprobar migraciones y configuración del framework.
- Revisar que no se hayan incluido secretos ni datos sensibles.
- Documentar cualquier verificación que no se haya podido ejecutar.
