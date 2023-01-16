
from unittest import mock
import json
import base64
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import DogPic
from .serializers import DogPicSerializer
from django.core.management import call_command


def mocked_requests_get(*args, **kwargs):
  class MockResponse:
    def __init__(self, content, status_code):
      self.content = content
      self.status_code = status_code

  if args[0] == 'https://dog.ceo/api/breeds/image/random/24':
    return MockResponse(json.dumps({
        "status": "success",
        "message": [
            f"https://images.dog.ceo/dog_pic_{i}.jpg" for i in range(24)
        ]
    }), 200)
  else:
    return MockResponse(base64.decodebytes(b'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAV3q5AA=='), 200)


def mocked_random_choice(*args, **kwargs):
  return args[0][10]


class DogPicTests(APITestCase):

  @mock.patch('requests.get', side_effect=mocked_requests_get)
  def test_populate_db(self, *args, **kwargs):
    """
    Ensure that the db populates if the dog.ceo requests are successful
    """
    margs = []
    mopts = {}
    call_command('populate_db', *margs, **mopts)
    self.assertEqual(DogPic.objects.count(), 24)

  @mock.patch('requests.get', side_effect=mocked_requests_get)
  @mock.patch('dogs.views.choice', side_effect=mocked_random_choice)
  def test_retrieve(self, *args, **kwargs):
    """
    Ensure we can retrieve dog pics.
    """
    margs = []
    mopts = {}
    call_command('populate_db', *margs, **mopts)
    url = reverse('random_dog')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data,
                     {'original': '/media/10.jpg',
                      'modified': '/media/10_bw.jpg',
                         'metadata': {
                             'url': 'https://images.dog.ceo/dog_pic_10.jpg',
                             'info': {'dpi': [0.0, 0.0], 'compression': 0},
                             'mode': 'RGB',
                             'size': [1, 1],
                             'width': 1,
                             'format': None,
                             'height': 1,
                             'palette': None
                         }
                      }
                     )
