from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from audit.models import AuditEvent


class AuditedAuthTokenView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if not serializer.is_valid():
            AuditEvent.objects.create(
                action="authentication.login",
                result=AuditEvent.Result.DENIED,
                source="android",
                correlation_id=request.correlation_id,
                ip_address=request.META.get("REMOTE_ADDR"),
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
            ip_address=request.META.get("REMOTE_ADDR"),
        )
        return Response({"token": token.key})
