from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


class JWTCookieMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'])
        if token:
            try:
                at = AccessToken(token)
                _ = at.payload.get('user_id')
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            except TokenError:
                pass
        response = self.get_response(request)

        return response
