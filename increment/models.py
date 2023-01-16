from django.db import models

# Create your models here.
class KeyValuePair(models.Model):
    key = models.CharField(unique=True,max_length=50,null=False,blank=False)
    value = models.IntegerField(default=0,null=False,blank=True)