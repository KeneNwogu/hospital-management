import jwt
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from hospital_ms import settings

from functools import wraps
from graphql import GraphQLError


def require_authentication(func):
    @wraps(func)
    def wrapper(cls, root, info, input):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("Authentication required to perform this action")
        return func(cls, root, info, input)
    return wrapper


class AuthMiddleware:
    def resolve(self, next, root, info, *args, **kwargs):
        context = info.context.headers
        token = context.get('Authorization')

        if token is None:
            return next(root, info, *args, **kwargs)

        token = token.split(' ')
        if len(token) != 2 or token[0] != 'Bearer':
            raise AuthenticationFailed('Invalid Authentication token')
        token = token[1]

        try:
            user_payload = jwt.decode(token, settings.SECRET_KEY, settings.JWT_ENCRYPTION_METHOD)
        except (jwt.exceptions.InvalidSignatureError, jwt.ExpiredSignatureError, jwt.exceptions.DecodeError) as e:
            raise AuthenticationFailed('Invalid Authentication token')
        else:
            user_id = user_payload.get('user_id')
            try:
                user = get_user_model().objects.get(id=user_id)
            except get_user_model().DoesNotExist:
                raise AuthenticationFailed('Invalid user token')
            else:
                info.context.user = user
        return next(root, info, *args, **kwargs)
