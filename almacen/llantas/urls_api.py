from rest_framework.routers import DefaultRouter
from .views import ValeViewSet, LlantaViewSet, EconomicoViewSet, MovimientoViewSet
from general.views import ProductoViewSet

router = DefaultRouter()
router.register(r'vale', ValeViewSet, basename='vale')
router.register(r'llanta', LlantaViewSet, basename='llanta')
router.register(r'economico', EconomicoViewSet, basename='economico')
router.register(r'movimiento', MovimientoViewSet, basename='movimiento')
router.register(r'producto', ProductoViewSet, basename='producto')
urlpatterns = router.urls