from rest_framework import routers

from restaurants.views.category import CategoryManageViewSet
from restaurants.views.kitchen import KitchenViewSet, KitchenManageViewSet
from restaurants.views.product import ProductReadOnlyViewSet, ProductManageViewSet
from restaurants.views.product_portion import ProductPortionManageViewSet
from restaurants.views.restraurant import RestaurantReadOnlyViewSet, RestaurantManageViewSet

router = routers.SimpleRouter()

# Public API
router.register('rest', RestaurantReadOnlyViewSet, basename='rest')
router.register('products', ProductReadOnlyViewSet, basename='products')
router.register('kitchens', KitchenViewSet, basename='kitchens')

# Manage API
router.register('rest-manage', RestaurantManageViewSet, basename='rest-manage')
router.register('categories-manage', CategoryManageViewSet, basename='categories-manage')
router.register('products-manage', ProductManageViewSet, basename='products-manage')
router.register('kitchens-manage', KitchenManageViewSet, basename='kitchens-manage')
router.register('product-portions-manage', ProductPortionManageViewSet, basename='product-portions-manage')

urlpatterns = router.urls
