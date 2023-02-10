from django.urls import path, include
from app_v1.views import ItemViewSet,  OrderProductsViewSet, OrdersViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api_v2'

router = DefaultRouter()
router.register('items', ItemViewSet)
router.register('orders', OrdersViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', obtain_auth_token, name='api_token_auth'),
]