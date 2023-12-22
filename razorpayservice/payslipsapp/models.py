from django.db import models
from authapp.models import CustomUser
from django.contrib.postgres.fields import ArrayField

class Payslips(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,unique=True)
    salary = models.IntegerField(blank=False)
    deductions = models.IntegerField(blank=False)
    payslip_docs = ArrayField(models.CharField(max_length=255, blank=True), null=True, default=list)
    
    def __str__(self):
        return self.uploaded_on.date()