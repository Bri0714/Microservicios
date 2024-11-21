from django.contrib.auth import get_user_model, authenticate
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .serializers import (
    UserRegisterSerializer, UserLoginSerializer, UserSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from rest_framework import generics


UserModel = get_user_model()

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'La contraseña ha sido restablecida exitosamente.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generar token JWT
            payload = {
                'user_id': user.user_id,
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow(),
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            return Response({'message': 'Usuario creado exitosamente.', 'token': token}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                # Generar token JWT
                payload = {
                    'user_id': user.user_id,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow(),
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({'token': token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Credenciales incorrectas.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # No es necesario manejar tokens aquí, ya que con JWT no almacenamos tokens en el servidor
        return Response({'message': 'Sesión cerrada exitosamente.'}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Perfil actualizado exitosamente.',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)