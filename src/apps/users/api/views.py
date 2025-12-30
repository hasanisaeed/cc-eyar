from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from apps.users.api.serializers import UserRegisterSerializer
from apps.users.application.services import UserService


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=UserRegisterSerializer, responses={201: UserRegisterSerializer})
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserService.register_user(serializer.validated_data)

        return Response(
            {"message": "User registered successfully", "email": user.email},
            status=status.HTTP_201_CREATED
        )
