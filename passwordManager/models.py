from django.db import models

# Create your models here.
#      print(Website,Username,Password)

class Credentials(models.Model):
    website = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.website