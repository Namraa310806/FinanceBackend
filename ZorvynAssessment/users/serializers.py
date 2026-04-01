from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of user profile data."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'is_active',
            'first_name',
            'last_name',
            'created_at',
        )
        read_only_fields = ('id', 'is_active', 'created_at')


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for public user registration."""

    role = serializers.ChoiceField(
        choices=User.Role.choices,
        required=False,
        default=User.Role.VIEWER,
        error_messages={
            'invalid_choice': 'Role must be VIEWER, ANALYST, or ADMIN.',
        },
    )
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            'required': 'Password is required.',
            'min_length': 'Password must be at least 8 characters long.',
        },
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'role', 'first_name', 'last_name')

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def create(self, validated_data):
        validated_data.setdefault('role', User.Role.VIEWER)
        return User.objects.create_user(**validated_data)


class AdminUserManagementSerializer(serializers.ModelSerializer):
    """Serializer used by admin-only user management endpoints."""

    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
            'role',
            'is_active',
            'first_name',
            'last_name',
            'created_at',
        )
        read_only_fields = ('id', 'created_at')

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_email(self, value):
        queryset = User.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    def validate_username(self, value):
        queryset = User.objects.filter(username__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginTokenObtainPairSerializer(TokenObtainPairSerializer):
    """JWT serializer with additional user context in token and response."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        if not self.user.is_active:
            raise serializers.ValidationError('This account is inactive.')

        data['user'] = UserSerializer(self.user).data
        return data
