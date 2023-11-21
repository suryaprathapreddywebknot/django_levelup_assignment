

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import FileUploadSerializer
from rest_framework.permissions import IsAuthenticated

class FileUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=FileUploadSerializer,
        responses={status.HTTP_200_OK: 'File uploaded successfully', status.HTTP_400_BAD_REQUEST: 'Bad Request'},
        operation_description="uploads documents",
        tags=['Documents'],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # you can access the file like this from serializer
            # uploaded_file = serializer.validated_data["file"]
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
