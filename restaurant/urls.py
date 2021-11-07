from rest_framework import routers

from restaurant.views import RestaurantViewSet, CategoryViewSet


router = routers.SimpleRouter()

router.register(r'', RestaurantViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products', CategoryViewSet)

urlpatterns = router.urls
