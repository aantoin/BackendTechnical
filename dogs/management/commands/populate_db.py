import os
from io import BytesIO
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import requests
import logging
import json
from PIL import Image,ImageEnhance,UnidentifiedImageError
from PIL.ExifTags import TAGS
from dogs.models import DogPic

class Command(BaseCommand):
    help = 'Populates the database with two dozen dog images'

    def handle(self, *args, **options):
        DogPic.objects.all().delete()
        logger = logging.getLogger(__name__)
        numToFetch = max(0,24-DogPic.objects.count())
        try:
            im = requests.get('https://dog.ceo/api/breeds/image/random/24')
        except ConnectionError:
            logger.error(f'Could not connect to dog.ceo')
        if im.status_code != 200:
            logger.error("Error fetching urls from dog.ceo")
            return
        try:
            im = json.loads(im.content)
        except json.JSONDecodeError:
            logger.error("Invalid list response from dog.ceo")
            return
        urls = im.get('message')
        if not urls:
            logger.error("No results returned from dog.ceo")
            return
        for i,url in enumerate(urls):
            try:
                im = requests.get(url)
            except ConnectionError:
                logger.error(f'Could not connect to {url}')
                continue
            if im.status_code != 200:
                logger.error(f"Could not fetch {url}")
                return
            # Images
            try:
                im = Image.open(BytesIO(im.content))
            except UnidentifiedImageError:
                logger.error(f"Could not parse {url}")
                continue
            original_fn = f'{i}.jpg'
            modified_fn = f'{i}_bw.jpg'
            Path(os.path.join(settings.MEDIA_ROOT,original_fn)).parent.mkdir(exist_ok=True, parents=True)
            im.save(os.path.join(settings.MEDIA_ROOT,original_fn))
            im = ImageEnhance.Color(im).enhance(0)
            im.save(os.path.join(settings.MEDIA_ROOT,modified_fn))
            # Metadata
            metadata = {'url':url}
            for attr in ['format','mode','size','width','height','palette','info','is_animated','n_frames',]:
                if hasattr(im,attr):
                    metadata[attr] = getattr(im, attr)
            exifdata = im.getexif()
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode()
                metadata[tag]=data
            dogPic = DogPic(original = original_fn, modified=modified_fn,metadata=metadata)
            dogPic.save()
        
