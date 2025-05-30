from rest_framework import  serializers
from rest_framework.validators import ValidationError
from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email  = serializers.EmailField(max_length=80)
    username =  serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email_exists  = attrs.get('email')

        if User.objects.filter(email=email_exists):
            raise ValidationError('Email has already been used')
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user