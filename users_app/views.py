from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from.serializers import SignUpSerializer
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request
from .tokens import  create_jwt_pair_for_user

class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request:Request):
        data = request.data

        serializer = self.serializer_class(data= data)
        if  serializer.is_valid():
            serializer.save()
            response  = {'message': 'User  Created successfully'}
            return Response(data= response, status = status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')
        user= authenticate(email=email, password=password)

        if user is not None:
            tokens = create_jwt_pair_for_user(user)
            response  = {
                'message': 'Login is successful',
                'tokens': tokens
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data={'message':'Invalid login'})

    def get(selfself, request=Request):
        content = {
            'user':str(request.user),
            'auth':str(request.auth)
        }
        return Response(data=content, status=status.HTTP_200_OK)
