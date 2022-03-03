from django.db import models

# Create your models here.


class Credentials(models.Model):
    website = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    login_user = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.website