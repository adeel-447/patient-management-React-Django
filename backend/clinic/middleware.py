import json
import time
import uuid
from logging import getLogger


audit_logger = getLogger("clinic.audit")


class RequestIdAuditLoggingMiddleware:
    """
    Adds/propagates a request ID and emits a structured audit log line
    for every request without logging sensitive payload data.
    """

    request_id_header = "HTTP_X_REQUEST_ID"
    response_header = "X-Request-ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started_at = time.monotonic()

        request_id = request.META.get(self.request_id_header) or str(uuid.uuid4())
        request.request_id = request_id

        response = self.get_response(request)
        response[self.response_header] = request_id

        duration_ms = int((time.monotonic() - started_at) * 1000)
        user_id = request.user.id if getattr(request.user, "is_authenticated", False) else None
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
        client_ip = (
            forwarded_for.split(",")[0].strip()
            if forwarded_for
            else request.META.get("REMOTE_ADDR")
        )

        audit_payload = {
            "event": "http_request",
            "request_id": request_id,
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "user_id": user_id,
            "client_ip": client_ip,
        }
        audit_logger.info(json.dumps(audit_payload, sort_keys=True))

        return response
