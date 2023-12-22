from django.urls import path
from .views import PayslipView,PayslipUpdateView,PayslipsGetView

app_name = 'api'

urlpatterns = [
    path('payslip/create/', PayslipView.as_view(), name='payslipcreate'),
    path('payslip/update/<int:pk>/', PayslipUpdateView.as_view(), name='payslipupdate'),
    path('payslip/all/', PayslipsGetView.as_view(), name='payslipsget'),
   
]