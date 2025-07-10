from math import ceil

from django.db import transaction
from django.core.cache import cache
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from app.models import (
    Message,
    Document,
)


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'username', 'content', 'published_at', 'modified_at']
        read_only_fields = ['id', 'user', 'published_at', 'modified_at']

    def get_username(self, obj):
        return obj.user.username if obj.user else None


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'is_staff']
        read_only_fields = ['username', 'is_staff']


class UserRegistrationSerializer(serializers.Serializer):

    username = serializers.EmailField(write_only=True, validators=[validate_email], required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs['username']
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This email is already in use.")
        user = User(username=username, email=username)
        validate_password(attrs['password'], user)
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password']
            )
        return user


class UsernameChangeSerializer(serializers.Serializer):

    username = serializers.EmailField(required=True, validators=[validate_email])

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.filter(username=value).exclude(username=user.username).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value


class PasswordChangeSerializer(serializers.Serializer):

    password = serializers.CharField(validators=[validate_password], required=True)


class PasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(validators=[validate_email], required=True)

    def validate_email(self, value):
        token = cache.get(f'password_reset:email:{value}')
        ttl = cache.ttl(f'password_reset:email:{value}')
        if token is not None and ttl is not None and ttl > 0:
            raise serializers.ValidationError(f"This email has already been requested. Please try again in {ceil(ttl / 60)} minutes.")
        return value


class PasswordResetSerializer(serializers.Serializer):

    token = serializers.CharField(required=True)
    password = serializers.CharField(validators=[validate_password], required=True)

    def validate_token(self, value):
        email = cache.get(f'password_reset:token:{value}')
        ttl = cache.ttl(f'password_reset:token:{value}')
        if not email:
            raise serializers.ValidationError("Invalid token.")
        if ttl is None or ttl <= 0:
            raise serializers.ValidationError("Invalid token.")
        if not User.objects.filter(username=email).exists():
            raise serializers.ValidationError("Invalid token.")
        self.context['email'] = email
        return value


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = [
            'id',
            'title',
            'content',
            'published_at',
            'modified_at',
        ]
        read_only_fields = [
            'id',
            'published_at',
        ]
