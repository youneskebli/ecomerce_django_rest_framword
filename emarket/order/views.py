from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework import status

from product.models import Product
from .serializers import OrderSerializer
from .models import Order,OrderItems
# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    orders= Order.objects.all()
    serializer= OrderSerializer(orders,many=True)
    return Response({"orders":serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_one_order(request,pk):
    order= get_object_or_404(Order, id=pk)
    serializer= OrderSerializer(order,many=False)
    return Response({"orders":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    data=request.data
    user=request.user
    order_items=data['order_items']

    if order_items and len(order_items) == 0:
        return Response({'error':'no order recieved'},status=status.HTTP_400_BAD_REQUEST)
    else:
        total_amount=sum(item['price']*item['quantity'] for item in order_items)
        order= Order.objects.create(
            user =user,
            city= data['city'],
            zip_code=data['zip_code'],
            street=data['street'],
            phone_number=data['phone_number'],
            country=data['country'],
            total_amount=total_amount,
        )

        for i in order_items:
            product= get_object_or_404(Product,id=i['product'])
            item= OrderItems.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=i['quantity'],
                price=product.price
            )
            product.stock -= item.quantity
            product.save()
        serializer= OrderSerializer(order,many=False)
        return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_order_status(request,pk):
    order= get_object_or_404(Order, id=pk)
    order.status=request.data['status']
    order.save()
    serializer= OrderSerializer(order,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_order(request,pk):
    order=Order.objects.get(id=pk)
    order.delete()
    return Response({"details":"order is deleted"})

