from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from.serializers import SignUpSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import  create_jwt_pair_for_user


from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SMSVerificationSerializer
from .models import User, SMSVerification
from .serializers import  SignUpSerializer
from rest_framework import viewsets
from rest_framework import status

from .services.code_limited_service import is_code_limited, set_code_limited
from .services.validate_code import code_valid
from .tasks import generate_and_save_and_send_code


class UserApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        if is_code_limited(email):
            return Response({'error': 'Превышен лимит кодов.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = generate_and_save_and_send_code.delay(email)

        cache.set(f'sms_limit_{email}', code, timeout=300)
        print(f"Setting cache: key=sms_limit_{email}, value={code}, timeout=300")
        set_code_limited(email)  # Устанавливаем лимит отправки SMS

        return Response({'message': 'Код отправлен.'}, status=status.HTTP_201_CREATED)


class SMSVerificationApiView(viewsets.ModelViewSet):
    queryset = SMSVerification.objects.all()
    serializer_class = SMSVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = SMSVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        code = serializer.validated_data.get('code')

        if not email:
            return Response({'error': 'email обязателен.'}, status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({'error': 'Необходимо код подтверждения.'}, status.HTTP_400_BAD_REQUEST)

        # Проверяем код из кэша
        if not code_valid(email, code):
            return Response({'error': 'Код не валиден или истек.'}, status.HTTP_400_BAD_REQUEST)

        try:
            # Проверяем запись SMS
            verification = SMSVerification.objects.get(email=email, code=code, is_used=False)
            verification.is_used = True
            verification.save()

            # Проверяем или создаем пользователя
            user, created = User.objects.get_or_create(email=email)

            cache.delete(f'sms_code_{email}')

            refresh = RefreshToken.for_user(user)

            # Генерация токенов
            if created:
                return Response({
                    'message': 'Успешный вход!, хотите дополнить профиль?',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status.HTTP_201_CREATED)

            return Response({
                'message': 'Успешный вход!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Код не найден или уже использован.'}, status.HTTP_400_BAD_REQUEST)



# class SignUpApiView(viewsets.ModelViewset):
#     serializer_class = SignUpSerializer
#
#     def post(self, request:Request):
#         data = request.data
#
#         serializer = self.serializer_class(data= data)
#         if  serializer.is_valid():
#             serializer.save()
#             response  = {'message': 'User  Created successfully'}
#             return Response(data= response, status = status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#
#
# class LoginView(APIView):
#     def post(self, request:Request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user= authenticate(email=email, password=password)
#
#         if user is not None:
#             tokens = create_jwt_pair_for_user(user)
#             response  = {
#                 'message': 'Login is successful',
#                 'tokens': tokens
#             }
#             return Response(data=response, status=status.HTTP_200_OK)
#         return Response(data={'message':'Invalid login'})
#
#     def get(selfself, request=Request):
#         content = {
#             'user':str(request.user),
#             'auth':str(request.auth)
#         }
#         return Response(data=content, status=status.HTTP_200_OK)
