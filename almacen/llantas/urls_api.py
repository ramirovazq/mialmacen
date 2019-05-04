from rest_framework.routers import DefaultRouter
from .views import ValeViewSet, LlantaViewSet

router = DefaultRouter()
router.register(r'vale', ValeViewSet, basename='vale')
router.register(r'llanta', LlantaViewSet, basename='llanta')
urlpatterns = router.urls