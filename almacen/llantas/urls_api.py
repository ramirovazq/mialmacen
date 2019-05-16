from rest_framework.routers import DefaultRouter
from .views import ValeViewSet, LlantaViewSet, EconomicoViewSet

router = DefaultRouter()
router.register(r'vale', ValeViewSet, basename='vale')
router.register(r'llanta', LlantaViewSet, basename='llanta')
router.register(r'economico', EconomicoViewSet, basename='economico')
urlpatterns = router.urls