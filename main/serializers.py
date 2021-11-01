from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

from .models import CustomUser, UserProfile


class UserWithTokenSerializer(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only = True)
    refresh = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['username', 'is_staff', 'is_active', 'id', 'email', 'date_joined', 'is_superuser', 'access',
                  'refresh', 'first_name', 'last_name']

    def get_access(self, obj):
        token = RefreshToken.for_user(obj)

        token['username'] = obj.username
        token['name'] = obj.first_name
        token['id'] = obj.id
        token['is_staff'] = obj.is_staff
        token['avatar'] = 'static/images/default-profile.png'

        return str(token.access_token)

    def get_refresh(self, obj):
        token = RefreshToken.for_user(obj)

        return str(token)


# custom claims Token obtain.
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['name'] = user.first_name
        token['is_staff'] = user.is_staff
        token['id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserWithTokenSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


# user profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    
    loyaltyPoints = serializers.SerializerMethodField(read_only=True)
    HeaderImage = serializers.SerializerMethodField(read_only = True)
    Avatar = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = UserProfile
        fields = ['Country', 'Contact', 'HeaderImage', 'Avatar', 'loyaltyPoints']

    def get_loyaltyPoints(self, obj):
        return obj.loyaltyPoints

    def get_HeaderImage(self, obj):
        return obj.HeaderImage.url if obj.HeaderImage else None

    def get_Avatar(self, obj):
        return obj.Avatar.url if obj.Avatar else  None


# user serializer
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'id']


# profile images serializer
class ProfileImagesSerilizer(serializers.ModelSerializer):
    HeaderImage = serializers.SerializerMethodField(read_only = False)
    Avatar = serializers.SerializerMethodField(read_only = False)

    class Meta:
        model = UserProfile
        fields =['HeaderImage', 'Avatar']

    def get_IeaderImage(self, obj):
        return obj.HeaderImage.url if obj.HeaderImage else None

    def get_Avatar(self, obj):
        return obj.Avatar.url if obj.Avatar else None



# djoser
from djoser.serializers import UserCreateSerializer
class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "email", "username", "first_name", "last_name", "password")