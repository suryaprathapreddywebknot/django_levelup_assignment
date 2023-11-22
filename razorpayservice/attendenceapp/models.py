from django.db import models
from authapp.models import CustomUser

class Attendence(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    checkin = models.TimeField(blank=False)
    checkout = models.TimeField(blank=False)
    status=models.CharField(max_length=255,blank=False)
    duration=models.TimeField(blank=False)
    remarks=models.TextField(blank=False)
    isApprooved=models.BooleanField(default=False)
    
    def __str__(self):
        return self.uploaded_on.date()