from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import KeyValuePair
from .serializers import KeyValuePairSerializer


class KeyValuePairTests(APITestCase):
  def test_create(self):
    """
    Ensure we can create a new key value pair.
    """
    url = reverse('keyvaluepair-list')
    data = {'key': 'testkey'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(KeyValuePair.objects.count(), 1)
    self.assertEqual(KeyValuePair.objects.get().key, 'testkey')
    self.assertEqual(KeyValuePair.objects.get().value, 0)

  def test_create_with_start_value(self):
    """
    Ensure we can create a new key value pair with provided default.
    """
    url = reverse('keyvaluepair-list')
    values = [-10, 0, 2, 1000000000]
    for i in range(len(values)):
      data = {'key': 'testkey_'+str(values[i]), 'value': values[i]}
      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)
      self.assertEqual(KeyValuePair.objects.count(), i+1)
      self.assertEqual(KeyValuePair.objects.last().key,
                       'testkey_'+str(values[i]))
      self.assertEqual(KeyValuePair.objects.last().value, values[i])

  def test_create_with_duplicate_key(self):
    """
    Ensure we cannot overwrite an existing key value pair.
    """
    url = reverse('keyvaluepair-list')
    data = {'key': 'testkey'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(KeyValuePair.objects.count(), 1)
    url = reverse('keyvaluepair-list')
    data = {'key': 'testkey', 'value': 10}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(KeyValuePair.objects.count(), 1)
    self.assertEqual(KeyValuePair.objects.get().key, 'testkey')
    self.assertEqual(KeyValuePair.objects.get().value, 0)

  def test_list(self):
    """
    Ensure we can list key value pairs.
    """
    # list empty
    url = reverse('keyvaluepair-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertListEqual(response.data, [])
    # create data 1
    data = {'key': 'testkey', 'value': 42}
    response = self.client.post(url, data, format='json')
    # list 1 item
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, [{'id': response.data[0]['id'], **data}])
    # create data 2
    data2 = {'key': 'testkey2'}
    response = self.client.post(url, data2, format='json')
    # list 2 items
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(
        response.data, [{'id': response.data[0]['id'], **data}, {'id': response.data[1]['id'], 'value': 0, **data2}])

  def test_increment(self):
    """
    Ensure we can increment a key value pair
    """
    # create data 1
    url = reverse('keyvaluepair-list')
    data = {'key': 'testkey', 'value': 42}
    response = self.client.post(url, data, format='json')
    # create data 2
    url = reverse('keyvaluepair-list')
    data2 = {'key': 'testkey2', 'value': 42}
    response = self.client.post(url, data2, format='json')
    # increment existing key
    url = reverse('keyvaluepair-increment')
    response = self.client.post(url, {'key': data['key']}, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data, {'success': True})
    # Check Objects
    pairs = KeyValuePair.objects.all().order_by('key')
    self.assertEqual(KeyValuePairSerializer(pairs[0]).data, {
                     'id': KeyValuePairSerializer(pairs[0]).data['id'], 'key': data['key'], 'value': data['value']+1})
    self.assertEqual(KeyValuePairSerializer(pairs[1]).data, {
                     'id': KeyValuePairSerializer(pairs[1]).data['id'], 'key': data2['key'], 'value': data2['value']})
    # increment non-existing key
    url = reverse('keyvaluepair-increment')
    response = self.client.post(url, {'key': 'badkey'}, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(response.data, {'success': False})
    # Check Objects
    pairs = KeyValuePair.objects.all().order_by('key')
    self.assertEqual(KeyValuePairSerializer(pairs[0]).data, {
                     'id': KeyValuePairSerializer(pairs[0]).data['id'], 'key': data['key'], 'value': data['value']+1})
    self.assertEqual(KeyValuePairSerializer(pairs[1]).data, {
                     'id': KeyValuePairSerializer(pairs[1]).data['id'], 'key': data2['key'], 'value': data2['value']})
