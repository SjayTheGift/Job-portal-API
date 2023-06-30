from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, status, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView # new
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LogInSerializer, 
    # UserCreateSerializer, 
    # UserProfileSerializer,
    EducationSerializer,
    DeveloperSerializer,
    DeveloperSignUpSerializer,
    ClientSignUpSerializer
)
from .models import Developer, Education

User = get_user_model()

# class SignUpView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer


class DeveloperSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = DeveloperSignUpSerializer


class ClientSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ClientSignUpSerializer


class LogInView(TokenObtainPairView): # new
    serializer_class = LogInSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DeveloperProfileView(mixins.ListModelMixin,
                generics.GenericAPIView):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer
    # permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DeveloperProfileDetailView(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
                    
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

