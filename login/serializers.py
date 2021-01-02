#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from login.models import StaffProfile


User = get_user_model()

# Register Serializer for user registration

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'unique_id', 'staff_position', 'username', 'password', 'password2', 'email', 'first_name', 'last_name')
        # extra_kwargs = {'first_name': {'write_only': True}, 'last_name': {'write_only': True}

    def validate(self, attrs):
        username = attrs.get('username', '')
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match"})

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            staff_position=validated_data['staff_position'],
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# User Serializer for user list and delete user views
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True, 'required': True}} # this hides password from being seen

    def create(self, validated_data):   # this creates harshed password
        user = User.objects.create_user(**validated_data)
        return user


# update user model data
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': "This email already exists"})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': "This username already exists"})
        return value

    def update(self, instance, validated_data):
        # add checkpoint, logged in user only must be updated
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to update this user"})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()
        return instance


# change password

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match"})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': "old Password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to change this user's password"})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# serializer for extended user profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = "__all__"

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response


# update extended user profile

class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = ['middle_name', 'birthday', 'gender', 'country', 'profile_picture']

    def update(self, instance, validated_data):
        # add checkpoint, logged in user only must be updated
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to change this user's password"})

        instance.middle_name = validated_data['middle_name']
        instance.birthday = validated_data['birthday']
        instance.gender = validated_data['gender']
        instance.country = validated_data['country']
        instance.profile_picture = validated_data['profile_picture']

        instance.save()
        return instance


# logout serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({'bad_token': "Token is expired or invalid"})
