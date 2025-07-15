from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializer, UserSerializer


class UserVieSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["create", "register"]:
            return [AllowAny()]

        return [IsAuthenticated()]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        user = RegisterSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user = user.save()
        return Response(
            UserSerializer(user).data, status=status.HTTP_201_CREATED
        )
