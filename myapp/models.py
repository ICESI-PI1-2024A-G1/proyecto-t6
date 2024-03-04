from django.db import models

# Create your models here.
class Project(models.Model):
    name= models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name

class Tast(models.Model):
    tittle = models.CharField(max_length = 200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete = models.CASCADE)

    def __str__(self):
        return self.tittle