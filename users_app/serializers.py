from rest_framework import  serializers
from rest_framework.validators import ValidationError
# from rest_framework.authtoken.models import Token
from .models import User, SMSVerification


class SignUpSerializer(serializers.ModelSerializer):
    email  = serializers.EmailField(max_length=80, required=True, error_messages={'required':"Необходимо указать email"})

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_staff', 'image']

    def validate_email_exists(self, value):
        email_exists  = value.get('email')

        if User.objects.filter(email=email_exists):
            raise ValidationError('Email has already been used')
        return super().validate(value)

    # def create(self, validated_data):
    #     password = validated_data.pop('password')
    #     user = super().create(validated_data)
    #     user.set_password(password)
    #     user.save()
    #     Token.objects.create(user=user)
    #     return user


class SMSVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSVerification
        fields = ['id', 'email']

        def validate(self, value):
            if not value.get('email'):
                raise  serializers.ValidationError({'email': 'Необходимо указать email'})
            if not  value.get('code'):
                raise serializers.ValidationError({'code':'Необходимо указать код'})
            return value