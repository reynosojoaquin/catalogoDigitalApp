FROM python:3.13.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system app && adduser --system --ingroup app app
RUN apt-get update \
    && apt-get install --no-install-recommends --yes gettext=0.23.1-2 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements/base.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt

COPY --chown=app:app . /app
RUN for file in $(find /app/locale -name '*.po'); do msgfmt "$file" -o "${file%.po}.mo"; done \
    && chown -R app:app /app/locale
RUN mkdir -p /app/staticfiles && chown app:app /app/staticfiles
COPY --chmod=755 entrypoint.sh /usr/local/bin/catalogo-digital-entrypoint
ENV DJANGO_RUNTIME_LOCALE_PATH=/tmp/catalogo-digital-locale
ENTRYPOINT ["/usr/local/bin/catalogo-digital-entrypoint"]
USER app

FROM base AS development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
