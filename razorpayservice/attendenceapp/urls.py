from django.urls import path
from .views import AttendenceView,AttendenceUpdateView

app_name = 'api'

urlpatterns = [
    path('attendence/create/', AttendenceView.as_view(), name='attendence'),
    path('attendence/<int:pk>/', AttendenceUpdateView.as_view(), name='attendence-detail')
]