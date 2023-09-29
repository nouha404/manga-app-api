from django.db import models


# Create your models here.


class Informations(models.Model):
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    author = models.CharField(max_length=255)
    resume = models.TextField()
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.author} - {self.release_date}"


class Pages(models.Model):
    informations = models.ForeignKey(Informations, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    chapters = models.JSONField()
    
