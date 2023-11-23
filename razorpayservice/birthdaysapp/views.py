from django.shortcuts import render
from authapp.models import CustomUser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import date
from django.http import JsonResponse


class BirthdaysView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self,request):
        today = date.today()
        users = CustomUser.objects.filter(dob__day=today.day, dob__month=today.month).values('id','name','email','mobile','dob','role')
        customers_list = list(users)
        return JsonResponse(customers_list, safe=False)
