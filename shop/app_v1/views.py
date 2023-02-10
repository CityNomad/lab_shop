from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from app_v1.serializers import ItemSerializer, OrderSerializer, CartSerializer
from webapp.models import Item, Order, ItemsOrders


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser)

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticatedOrReadOnly()]
        return super().get_permissions()


class OrdersViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.order.user == request.user


class CartViewSet(ModelViewSet):
    queryset = ItemsOrders.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsOwnerOrReadOnly,)
