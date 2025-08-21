from django.db import models

class Credentials(models.Model):
    website = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.TextField()
    login_user = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.website
