from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .filters import ProductsFilter
from rest_framework import status



# Create your views here.
@api_view(['GET'])
def get_products(request):
    filterset= ProductsFilter(request.GET,queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPage = 6
    paginator = PageNumberPagination()
    paginator.page_size = resPage

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializer(queryset, many=True)
    return Response({"products": serializer.data, "per page": resPage, "count": count})

@api_view(['GET'])
def get_product_by_id(request,pk):
    product= get_object_or_404(Product,id=pk)
    serializer=ProductSerializer(product,many=False)
    return Response({"product":serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data = request.data
    serializer = ProductSerializer(data=data)

    if serializer.is_valid():
        product = Product.objects.create(**data, user=request.user)
        res = ProductSerializer(product, many=False)
        return  Response({"product":res.data})
    else:
        return Response(serializer.errors)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request,pk):
    product= get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({"error": "Sorry you can not update this product"}
                        , status=status.HTTP_403_FORBIDDEN)
    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.ratings = request.data['ratings']
    product.stock = request.data['stock']

    product.save()
    serializer= ProductSerializer(product,many=False)
    return Response({"product":serializer.data})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
    product= get_object_or_404(Product,id=pk)
    if product.user != request.user:
        return Response({"error": "Sorry you can not update this product"}
                        , status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({"details":"Delete action is done"},status=status.HTTP_200_OK)



#products= Product.objects.all()
#serializer= ProductSerializer(products,many=True)
#return Response({"Products":serializer.data})
