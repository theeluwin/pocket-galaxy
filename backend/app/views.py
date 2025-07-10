from uuid import uuid4

from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from app.tasks import send_email
from app.serializers import (
    UserProfileSerializer,
    UserRegistrationSerializer,
    UsernameChangeSerializer,
    PasswordChangeSerializer,
    PasswordRequestSerializer,
    PasswordResetSerializer,
)


User = get_user_model()


class APITokenLoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        response_super = super().post(request, *args, **kwargs)
        response = Response({}, status=status.HTTP_200_OK)
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            response_super.data.get('refresh', None),
            httponly=True,
        )
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],
            response_super.data.get('access', None),
            httponly=True,
        )
        return response


class APITokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], '')
        data = {
            'refresh': refresh,
        }
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        token = serializer.validated_data
        response = Response({}, status=status.HTTP_200_OK)
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            token['refresh'],
            httponly=True,
        )
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'],
            token['access'],
            httponly=True,
        )
        return response


class APITokenLogoutView(TokenBlacklistView):

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], '')
        data = {
            'refresh': refresh,
        }
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response({}, status=status.HTTP_200_OK)
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
        response.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_ACCESS'])
        return response


@api_view(['GET'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_health(request):
    return Response({})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_websocket_ticket(request):
    ticket = str(uuid4())
    user_id = request.user.id
    cache.set(f'websocket:ticket:{ticket}', user_id, settings.WEBSOCKET_TICKET_TTL)
    return Response({
        'ticket': ticket,
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_user_register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        _ = serializer.save()
        return Response({
            'message': "Registration completed successfully."
        }, status=status.HTTP_201_CREATED)
    error = "Registration failed."
    for _, values in serializer.errors.items():
        for error in values:
            break
    return Response({
        'error': error,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        user = request.user
        if 'username' in request.data:
            serializer = UsernameChangeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user.username = serializer.validated_data['username']
                user.save()
                return Response({
                    'message': "Email changed successfully.",
                })
            return Response({
                'error': serializer.errors['username'][0]
            }, status=status.HTTP_400_BAD_REQUEST)
        if 'password' in request.data:
            serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                user.set_password(serializer.validated_data['password'])
                user.save()
                return Response({
                    'message': "Password changed successfully."
                })
            return Response({
                'error': serializer.errors['password'][0]
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'error': "Please enter the information to change."
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_user_password_request(request):
    serializer = PasswordRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        token = str(uuid4())
        cache.set(f'password_reset:email:{email}', token, settings.EMAIL_RETRY_DELAY)
        if User.objects.filter(username=email).exists():
            cache.set(f'password_reset:token:{token}', email, settings.EMAIL_RETRY_DELAY)
            link_href = f"{settings.PROTOCOL}://{settings.HOST}/password/reset/?token={token}"
            link_content = "Password reset link"
            html_message = render_to_string('email/password_request.html', {
                'link_href': link_href,
                'link_content': link_content,
            })
            send_email.delay(
                f"[{settings.SITE_TITLE}] Password reset link",
                f"Password reset link: {link_href}",
                settings.EMAIL_HOST_USER,
                [email],
                html_message=html_message,
            )
        return Response({
            'message': "Password reset link sent to email."
        }, status=status.HTTP_201_CREATED)
    error = "Failed to send password reset link."
    for _, values in serializer.errors.items():
        for error in values:
            break
    return Response({
        'error': error,
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_user_password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        token = serializer.validated_data['token']
        password = serializer.validated_data['password']
        email = serializer.context['email']
        user = User.objects.get(username=email)
        user.set_password(password)
        user.save()
        cache.delete(f'password_reset:email:{email}')
        cache.delete(f'password_reset:token:{token}')
        return Response({
            'message': "Password changed successfully."
        }, status=status.HTTP_200_OK)
    error = "Password reset failed."
    for _, values in serializer.errors.items():
        for error in values:
            break
    return Response({
        'error': error,
    }, status=status.HTTP_400_BAD_REQUEST)
