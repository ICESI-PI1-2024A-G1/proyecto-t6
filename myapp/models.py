from django.db import models

# Create your models here.

class academy_Users_Credentials(models.Model):
    userName = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    def __str__(self):
        return self.userName