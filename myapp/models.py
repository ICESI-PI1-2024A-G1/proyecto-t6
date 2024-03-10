from django.db import models

# Create your models here.
class academic_members_information(models.Model):
    credential_academicMember = models.CharField(max_length=32)
    password_academicMember = models.CharField(max_length=16)
    def __str__(self):
        return self.credential_academicMember