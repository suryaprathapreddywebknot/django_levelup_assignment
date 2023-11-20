from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer,LoginSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema

class SignupView(APIView):
    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        responses={status.HTTP_201_CREATED: 'Token created successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Create a new user and return JWT tokens",
        tags=['Authentication'],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data) 
        if serializer.is_valid():
            # Hash the password before saving the user
            user = serializer.save(password=request.data.get('password'))
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={status.HTTP_200_OK: 'authorized', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Returns access token and jwt refresh token",
        tags=['Authentication'],
    )
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=data)
            if serializer.is_valid():
                email = serializer.validated_data.get('email')
                password = serializer.validated_data.get('password')
                user = authenticate(request, email=email, password=password)
                print(user)

                if user:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=status.HTTP_200_OK)
                else:
                    raise AuthenticationFailed('Invalid credentials')
            else:
                raise AuthenticationFailed('Invalid credentials')
        except AuthenticationFailed as e:
            return Response({
                'status': 400,
                'message': 'Invalid credentials',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({
                'status': 500,
                'message': 'An error occurred',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)