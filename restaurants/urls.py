from rest_framework import routers

from restaurants.views.category import CategoryRetrieveViewSet, CategoryManageViewSet
from restaurants.views.kitchen import KitchenViewSet
from restaurants.views.product import ProductReadOnlyViewSet
from restaurants.views.restraurant import RestaurantReadOnlyViewSet, RestaurantManageViewSet

router = routers.SimpleRouter()
router.register('rest', RestaurantReadOnlyViewSet)
router.register('rest-manage', RestaurantManageViewSet, basename='rm')
router.register('categories', CategoryRetrieveViewSet)
router.register('categories-manage', CategoryManageViewSet, basename='cm')
router.register('products', ProductReadOnlyViewSet)
router.register('kitchens', KitchenViewSet)
urlpatterns = router.urls
