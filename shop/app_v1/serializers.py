from django.contrib.auth import get_user_model
from rest_framework import serializers
from webapp.models import Item, Order, ItemsOrders


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'category', 'balance', 'price']
        read_only_fields = ['id', 'orders']


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'price']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']


class ItemsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsOrders
        fields = ["id", 'item', 'quantity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["item"] = NameSerializer(instance.item).data
        return data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "username", "phonenumber", "address", "created_at", "items", "user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["items"] = ItemsOrdersSerializer(instance.itemsorders.all(), many=True).data
        return data


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsOrders
        fields = ["id", "item", "quantity"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['item'] = NameSerializer(instance.item).data
        price = data['item']['price']
        quantity = data["quantity"]
        total = float(price) * quantity
        data['total'] = total
        return data
