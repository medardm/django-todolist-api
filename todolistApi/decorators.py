import jwt
from jwt.exceptions import InvalidTokenError
from django.http import JsonResponse
from todolistApi.settings import SECRET_JWT
from functools import wraps


# THIS IS NOT NEEDED ANYMORE, BUT WILL NOT DELETE IT BECAUSE IT'S A GOOD EXAMPLE ON HOW TO USE DECORATORS
def jwt_required(f=None, *, disallow_authenticated=False):
    def decorator(func):
        @wraps(func)
        def wrap(self, request, *args, **kwargs):
            if 'HTTP_COOKIE' in request.META:
                token = request.COOKIES.get('token')
                if token is not None:
                    try:
                        payload = jwt.decode(token, SECRET_JWT, algorithms='HS256')
                        request.user = payload
                        if disallow_authenticated and payload:
                            return JsonResponse({'error': 'You are not allowed to perform this action.'}, status=400)
                        return func(self, request, *args, **kwargs)
                    except InvalidTokenError:
                        if not disallow_authenticated:
                            return JsonResponse({'error': 'Invalid token. Please log in again.'}, status=401)
            if not disallow_authenticated:
                return JsonResponse({'error': 'You must be logged in to perform this action.'}, status=401)
            return func(self, request, *args, **kwargs)

        return wrap

    if f:
        return decorator(f)
    return decorator
