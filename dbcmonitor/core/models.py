from django.db import models
from django.utils.text import slugify


class Database(models.Model):
    name = models.CharField(max_length=64)
    slug = models.SlugField(max_length=64)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Database, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
