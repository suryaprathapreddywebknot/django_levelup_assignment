# from rest_framework import serializers
# from .models import Documents

# class UploadedFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Documents
#         fields = '__all__'

from rest_framework import serializers
from .models import Documents

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'