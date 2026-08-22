from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from .permissions import IsSeller
from .serializers import DeviceRegistrationSerializer, DeviceSerializer
from .services import DeviceOwnershipError, register_device


class DeviceRegistrationView(APIView):
    permission_classes = [IsSeller]

    def post(self, request):
        serializer = DeviceRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = register_device(
                user=request.user,
                device_id=serializer.validated_data["id"],
                platform=serializer.validated_data["platform"],
                app_version=serializer.validated_data["app_version"],
                correlation_id=request.correlation_id,
            )
        except DeviceOwnershipError:
            return Response(
                {"detail": _("The device is already registered to another account.")},
                status=status.HTTP_409_CONFLICT,
            )

        output = DeviceSerializer(result.device)
        response_status = status.HTTP_201_CREATED if result.created else status.HTTP_200_OK
        return Response(output.data, status=response_status)
