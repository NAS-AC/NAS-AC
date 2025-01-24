from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import DjangoUserSerializer, DjangoUserRegistrationSerializer
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DjangoUserRegistrationSerializer

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request, *args, **kwargs):
        logger.info("HEREEE")
        registration_serializer = DjangoUserRegistrationSerializer(data=request.data)

        if registration_serializer.is_valid():
            user = registration_serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': registration_serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)

        return Response(registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='verify-token')
    def verify_token(self, request):
        token = request.data.get('token')
        try:
            JWTAuthentication().get_validated_token(token)
            return Response({'message': 'Token is valid'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)