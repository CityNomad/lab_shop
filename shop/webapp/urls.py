from django.urls import path

from webapp.views import IndexView, ItemView, CreateItem, UpdateItem, DeleteItem, AddToCart, Cart, \
    OrderView, delete_one_by_one, Checkout, delete_from_cart

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('items/add/', CreateItem.as_view(), name="create_item"),
    path('item/<int:pk>/', ItemView.as_view(), name="item_view"),
    path('item/<int:pk>/update/', UpdateItem.as_view(), name="update_item"),
    path('item/<int:pk>/delete/', DeleteItem.as_view(), name="delete_item"),
    path('cart/<int:pk>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/', Cart.as_view(), name='cart'),
    path('cart/<int:pk>/delete/', delete_from_cart, name='delete_from_cart'),
    path('cart/<int:pk>/delete1/', delete_one_by_one, name='delete_one_from_cart'),
    path('checkout/', Checkout.as_view(), name='checkout'),
    path('orders/', OrderView.as_view(), name='orders'),
]
