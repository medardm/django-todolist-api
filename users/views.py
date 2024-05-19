import datetime

import jwt
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from todolistApi.permissions import IsSuperUser, IsNotAuthenticated
from todolistApi.settings import SECRET_JWT
from .serializers import UserSerializer, RegistrationSerializer

User = get_user_model()


class UserListView(APIView):
    permission_classes = [IsSuperUser, IsAuthenticated]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RegisterView(APIView):
    # permission_classes = [IsNotAuthenticated]

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data)  # Use UserSerializer just for the response
        return Response(serializer.errors)


class LoginView(APIView):
    # permission_classes = [IsNotAuthenticated]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me", False)
        user = authenticate(username=username, password=password)
        if user is not None:
            # Set token expiry based on remember_me flag
            dt = (datetime.datetime.now() + (datetime.timedelta(days=7) if remember_me
                                             else datetime.timedelta(minutes=15)))

            # refresh token will be valid for 7 days
            refresh_dt = datetime.datetime.now() + datetime.timedelta(days=7)

            token = jwt.encode({
                'id': user.id,
                'username': user.username,
                'is_superuser': user.is_superuser,
                'exp': int(dt.strftime('%s')),  # expiration time
                'iat': datetime.datetime.now(),
            }, SECRET_JWT, algorithm='HS256')

            refresh_token = jwt.encode({
                'id': user.id,
                'username': user.username,
                'exp': int(refresh_dt.strftime('%s')),  # expiration time
                'iat': datetime.datetime.now(),
            }, SECRET_JWT, algorithm='HS256')

            response = Response({
                "token": token,
                "refresh_token": refresh_token,
                "expires_at": dt.isoformat(),
                "remember": 'yes' if remember_me else 'no',
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": 'superuser' if user.is_superuser else 'staff'
                },
                "message": "Login successful"
            })
            response.set_cookie(
                'token',
                token,
                httponly=True,
                # secure=True,
                samesite='None',
                path='/'
            )

            return response

        else:
            return Response({"error": "Authentication Failed"}, status=HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):

        response = Response({"message": "Logout successful"})
        # Invalidate the token
        response.set_cookie('token', None)
        response.delete_cookie('token')

        return response


class ValidateTokenView(APIView):
    authentication_classes = []

    def post(self, request):
        token = request.COOKIES.get('token')
        response = None

        if not token:
            return Response({"error": "No token provided", "token_is_valid": False}, status=400)

        try:
            payload = jwt.decode(token, SECRET_JWT, algorithms='HS256')
            user = User.objects.filter(id=payload['id']).first()

            if user is None:
                response = Response({'error': 'Token is invalid, User not found!', "token_is_valid": False}, status=400)
            else:
                response = Response({'message': 'Token is valid', "token_is_valid": True}, status=200)

        except jwt.ExpiredSignatureError as e:
            response = Response({'error': 'Token has expired', "token_is_valid": False}, status=400)
        except jwt.DecodeError as e:
            response = Response({"error": "Invalid token", "token_is_valid": False}, status=400)

        if not response.data["token_is_valid"]:
            response.set_cookie('token', None)
            response.delete_cookie('token')

        return response
