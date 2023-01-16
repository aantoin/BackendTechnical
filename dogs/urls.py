from django.urls import path
from .views import BlackAndWhiteView

urlpatterns = [
    path('random/', BlackAndWhiteView.as_view(), name="random_dog"),
]
