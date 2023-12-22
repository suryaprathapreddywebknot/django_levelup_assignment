from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'mobile', 'role', 'otp', 'password','reset_token','created_at','dob')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            mobile=validated_data['mobile'],
            role=validated_data['role'],
            dob=validated_data['dob']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required.")

        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Assuming this is your CustomUser model
        fields = ['id', 'name', 'email', 'mobile','dob']