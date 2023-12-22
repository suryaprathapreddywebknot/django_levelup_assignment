from django.shortcuts import render
from .serializers import PayslipSerializer,PayslipGetSerializer,PayslipUpdateSerializer,PayslipCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .permissions import IsAdminPermission
from rest_framework.generics import get_object_or_404
from .models import Payslips

# Create your views here.
class PayslipView(APIView):
    permission_classes = [IsAuthenticated,IsAdminPermission]

    @swagger_auto_schema(
        request_body=PayslipCreateSerializer,
        responses={status.HTTP_201_CREATED: 'payslip created successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Used  to create payslip",
        tags=['Payslips'],
    )
    def post(self,request):
        data=request.data
        serializer=PayslipSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
        
class PayslipUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminPermission]
    @swagger_auto_schema(
        request_body=PayslipUpdateSerializer,
        responses={status.HTTP_200_OK: 'payslip updated successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Used  to create payslip",
        tags=['Payslips'],
    )
    def put(self, request, pk):
        payslip = get_object_or_404(Payslips, pk=pk)
        serializer = PayslipUpdateSerializer(payslip, data=request.data,context={'request': request})

        if serializer.is_valid():
            # Check if the user making the request is an admin
            if request.user.role == 'admin':
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({"detail": "You do not have permission to perform this action."},
                                status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PayslipsGetView(APIView):
    permission_classes = [IsAuthenticated,IsAdminPermission]
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: 'payslip fetched successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Fetches all payslips",
        tags=['Payslips'],
    )
    def get(self, request):
        # Retrieve all Payslip objects with associated User data using select_related
            payslips = Payslips.objects.select_related('user').all()
            
            # Serialize the list of Payslip objects, each including the User data
            serializer = PayslipGetSerializer(payslips, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)