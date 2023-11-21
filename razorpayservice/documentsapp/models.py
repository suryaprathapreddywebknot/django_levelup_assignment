from django.db import models
from authapp.models import CustomUser

# class Documents(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255,blank=False)
#     document = models.FileField(upload_to='uploads/',blank=False)

class Documents(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField()
    name = models.CharField(max_length=255,blank=False)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.uploaded_on.date()