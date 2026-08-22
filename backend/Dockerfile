FROM python:3.13-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app

COPY requirements/base.txt /tmp/requirements.txt
RUN pip install --requirement /tmp/requirements.txt

COPY --chown=app:app . /app
USER app

FROM base AS development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM base AS production
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]

