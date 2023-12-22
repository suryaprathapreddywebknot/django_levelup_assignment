from rest_framework import serializers
from .models import Payslips
from authapp.serializers import CustomUserSerializer

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslips
        fields = '__all__'

class PayslipCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslips
        fields = '__all__'
        read_only_fields = ['payslip_docs']


class PayslipUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslips
        fields = '__all__'
        read_only_fields = ['user','payslip_docs']

class PayslipGetSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    class Meta:
        model = Payslips
        fields = '__all__'

    


