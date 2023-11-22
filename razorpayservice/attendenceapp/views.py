from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AttendenceSerializer,AttendenceCreateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .permissions import IsAdminPermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Attendence

class AttendenceView(APIView):

    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=AttendenceCreateSerializer,
        responses={status.HTTP_201_CREATED: 'Attendence created successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Used  to create attendence",
        tags=['Attendence'],
    )
    def post(self,request):
        data=request.data
        serializer=AttendenceCreateSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
    

    
        
class AttendenceUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsAdminPermission]
    @swagger_auto_schema(
        request_body=AttendenceSerializer,
        responses={status.HTTP_200_OK: 'Attendence updated successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="Used to update attendence",
        tags=['Attendence'],
    )
    def put(self, request, pk):
        attendance = get_object_or_404(Attendence, pk=pk)
        serializer = AttendenceSerializer(attendance, data=request.data,context={'request': request})

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


