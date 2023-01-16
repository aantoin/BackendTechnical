import os
from io import BytesIO
from django.apps import AppConfig
from PIL import Image,ImageEnhance
from PIL.ExifTags import TAGS
import requests
import json


class DogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dogs'
            
