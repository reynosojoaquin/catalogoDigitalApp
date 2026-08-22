# Catálogo Digital

Plataforma de intermediación comercial con administración web, API central y aplicación Android offline para vendedores.

## Inicio rápido

1. Copiar `.env.example` como `.env` y reemplazar los secretos.
2. Ejecutar `docker compose build`.
3. Ejecutar `docker compose run --rm backend python manage.py migrate`.
4. Ejecutar `docker compose up`.
5. Consultar `http://localhost:8000/health/`.

## Decisiones iniciales

- Backend: Python, Django y Django REST Framework.
- Persistencia: PostgreSQL.
- Coordinación y caché: Redis.
- Idioma inicial: `es-DO`; arquitectura preparada para inglés.
- Zona horaria de presentación inicial: `America/Santo_Domingo`.
- Los servicios de datos están aislados de la red pública.
- La API deniega acceso por defecto; `/health/` es el único endpoint público inicial.

Consulta [AGENTS.md](AGENTS.md) para las reglas funcionales y técnicas del proyecto.
