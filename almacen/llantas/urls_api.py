from rest_framework.routers import DefaultRouter
from llantas.views_api import ValeViewSet, LlantaViewSet, EconomicoViewSet, MovimientoViewSet
from general.views_api import ProductoViewSet
from persona.views_api import ProfilePositionViewSet, ProfileBodegaViewSet, ProfileEconomicoViewSet

router = DefaultRouter()
router.register(r'vale', ValeViewSet, basename='vale')
router.register(r'llanta', LlantaViewSet, basename='llanta')
router.register(r'economico', EconomicoViewSet, basename='economico')
router.register(r'movimiento', MovimientoViewSet, basename='movimiento')
router.register(r'producto', ProductoViewSet, basename='producto')
router.register(r'profileposition', ProfilePositionViewSet, basename='profileposition')
router.register(r'profilebodega', ProfileBodegaViewSet, basename='profilebodega')
router.register(r'profileeconomico', ProfileEconomicoViewSet, basename='profileeconomico')
urlpatterns = router.urls