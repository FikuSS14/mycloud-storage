from rest_framework import serializers
from .models import User, File
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'login', 'full_name', 'email', 'is_admin', 'storage_path']
        read_only_fields = ['id', 'storage_path']  

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['login', 'full_name', 'email', 'password', 'password_confirm']
    
    def validate_login(self, value):
        """Логин: только латинские буквы и цифры, первый символ — буква, длина 4-20"""
        pattern = r'^[A-Za-z][A-Za-z0-9]{3,19}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Логин должен содержать 4-20 символов: латиница и цифры, первый символ — буква'
            )
        return value
    
    def validate_email(self, value):
        """Email: базовый формат через regex"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError('Некорректный формат email')
        return value
    
    def validate_password(self, value):
        """Пароль: минимум 6 символов, заглавная буква, цифра, спецсимвол"""
        if len(value) < 6:
            raise serializers.ValidationError('Пароль должен быть не менее 6 символов')
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну цифру')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы один спецсимвол')
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            login=validated_data['login'],
            full_name=validated_data['full_name'],
            email=validated_data['email'],
            password=password
        )
        return user

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'original_name', 'comment', 'size', 'upload_date', 'last_download_date', 'special_link']
        read_only_fields = ['id', 'size', 'upload_date', 'last_download_date', 'special_link']