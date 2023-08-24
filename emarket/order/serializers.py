from rest_framework import serializers
from .models import Order,OrderItems


class OderItemsSerilizer(serializers.ModelSerializer):
    class Meta:
        model= OrderItems
        fields= "__all__"

class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(method_name="get_order_items",read_only=True)
    class Meta:
        model= Order
        fields= "__all__"

    def get_order_items(self,obj):
        order_ietms= obj.orderitems.all()
        serializer = OderItemsSerilizer(order_ietms,many=True)
        return serializer.data
