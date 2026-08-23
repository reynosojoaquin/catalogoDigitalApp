import uuid

from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def health(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        cursor.fetchone()
    probe_key = f"health:{uuid.uuid4().hex}"
    cache.set(probe_key, "ok", timeout=5)
    if cache.get(probe_key) != "ok":
        raise RuntimeError("Cache health probe failed")
    cache.delete(probe_key)
    return JsonResponse({"status": "ok"})
