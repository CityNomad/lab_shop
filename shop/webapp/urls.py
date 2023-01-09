from django.urls import path
from webapp.models import Basket

from webapp.views import IndexView, ItemView, CreateItem, UpdateItem, DeleteItem, add_item_basket, BasketView, DeleteFromBasket, CreateOrder, delete_one_by_one


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('items/add/', CreateItem.as_view(), name="create_item"),
    path('item/<int:pk>/', ItemView.as_view(), name="item_view"),
    path('item/<int:pk>/update/', UpdateItem.as_view(), name="update_item"),
    path('item/<int:pk>/delete/', DeleteItem.as_view(), name="delete_item"),
    path('add/<int:pk>/',add_item_basket, name="add_item_basket"),
    path('basket/', BasketView.as_view(), name="basket_view"),
    path('basket/delete/<int:pk>/', DeleteFromBasket.as_view(), name="delete_from_basket"),
    path('basket/delete1/<int:pk>/', delete_one_by_one, name="delete_one_by_one"),
    path('basket/order', CreateOrder.as_view(), name="create_order"),
]
