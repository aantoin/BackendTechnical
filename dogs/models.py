from django.db import models

# Create your models here.
class DogPic(models.Model):
    url = models.CharField(max_length=100,null=False,blank=False)
    original = models.ImageField(null=False,blank=False)
    modified = models.ImageField(null=False,blank=False)
    metadata = models.JSONField(default=dict)