from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'phone', 'role', 'password', 'password2')
        extra_kwargs = {
            'full_name': {'required': True},
            'phone': {'required': True},
            'role': {'read_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        
        phone = attrs.get('phone', '')
        if phone and not phone.startswith('+992') or len(phone) != 13:
            raise serializers.ValidationError({"phone": "Телефон должен быть в формате +992XXXXXXXXX"})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            role='customer',
            is_approved=False
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'phone', 'role', 'is_approved', 'created_at')
        read_only_fields = ('id', 'created_at')


class UserManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'phone', 'role', 'is_approved', 'created_at')
        read_only_fields = ('id', 'created_at')

class UserApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_approved',)