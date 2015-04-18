from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=128)

    def __str__(self):
        return self.name
