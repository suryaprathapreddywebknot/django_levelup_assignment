from django.urls import path
from .views import BirthdaysView

app_name = 'api'

urlpatterns = [
    path('birthdays/', BirthdaysView.as_view(), name='birthday')
]