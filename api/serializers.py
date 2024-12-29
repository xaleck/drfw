from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Currency, Event


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']  

    def create(self, validated_data):
        
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, validated_data):
        
        user = authenticate(username=validated_data['username'],
            password=validated_data['password'],)
        print(user)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        self.context['user'] = user 
        return validated_data
    
    def create(self, validated_data):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)
        print(user)
        return {
            'username': validated_data["username"],
            'access': str(refresh.access_token),  # Access token
            'refresh': str(refresh)  # Refresh token
        }