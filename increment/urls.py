from rest_framework import routers
from .views import KeyValuePairViewSet


router = routers.SimpleRouter()
router.register(r'keyvaluepairs', KeyValuePairViewSet)
urlpatterns = router.urls