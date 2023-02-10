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
        fields = ['name']


class ItemsOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemsOrders
        fields = ['item', 'quantity']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
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
