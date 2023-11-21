# from django.urls import path
# from .views import FileUploadView

# urlpatterns = [
#     path('document/upload/', FileUploadView.as_view(), name='file-upload'),
# ]

from django.urls import path
from .views import FileUploadAPIView

app_name = 'api'

urlpatterns = [
    path('document/upload/', FileUploadAPIView.as_view(), name='upload-file'),
]
