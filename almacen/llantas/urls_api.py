from rest_framework.routers import DefaultRouter
from .views import ValeViewSet

router = DefaultRouter()
router.register(r'vale', ValeViewSet, basename='vale')
urlpatterns = router.urls