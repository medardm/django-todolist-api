from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from todolistApi.settings import SECRET_JWT
import jwt


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        User = get_user_model()

        # Token can be taken from request cookies instead of from header
        token = request.COOKIES.get('token')

        if not token:
            # if no token provided, authentication is not required
            return None

        try:
            payload = jwt.decode(token, SECRET_JWT, algorithms='HS256')
        except jwt.ExpiredSignatureError as e:
            # If the token has expired, an AuthenticationFailed exception will be raised.
            raise AuthenticationFailed('Token has expired')
        except jwt.DecodeError as e:
            # If the token is invalid
            return JsonResponse({"error": "Invalid token"}, status=401)

        user = User.objects.filter(id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        return (user, token)  # authentication successful
