import uuid


class AuditContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        supplied_id = request.headers.get("X-Correlation-ID", "")
        try:
            correlation_id = str(uuid.UUID(supplied_id))
        except (ValueError, AttributeError):
            correlation_id = str(uuid.uuid4())
        request.correlation_id = correlation_id
        response = self.get_response(request)
        response["X-Correlation-ID"] = correlation_id
        return response

