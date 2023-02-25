from rest_framework import routers
from .api import CardViewSet
from .views import CardGeneratorView

router = routers.DefaultRouter()
router.register('api/card', CardViewSet, 'card')



urlpatterns = router.urls
