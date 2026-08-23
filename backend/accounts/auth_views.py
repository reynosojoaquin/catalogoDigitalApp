from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle, ScopedRateThrottle

from audit.models import AuditEvent


class AuditedAuthTokenView(ObtainAuthToken):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "login"

    @staticmethod
    def client_ip(request):
        return BaseThrottle().get_ident(request)

    def throttled(self, request, wait):
        AuditEvent.objects.create(
            action="authentication.throttled",
            result=AuditEvent.Result.DENIED,
            source="android",
            correlation_id=request.correlation_id,
            ip_address=self.client_ip(request),
        )
        return super().throttled(request, wait)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            AuditEvent.objects.create(
                action="authentication.login",
                result=AuditEvent.Result.DENIED,
                source="android",
                correlation_id=request.correlation_id,
                ip_address=self.client_ip(request),
            )
            serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        AuditEvent.objects.create(
            actor=user,
            action="authentication.login",
            resource_type="user",
            resource_id=str(user.pk),
            result=AuditEvent.Result.SUCCESS,
            source="android",
            correlation_id=request.correlation_id,
            ip_address=self.client_ip(request),
        )
        return Response({"token": token.key, "user_id": str(user.pk)})
