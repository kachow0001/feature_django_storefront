from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()  # ORM
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})  
        # queryset will iterate and serialize each item
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # to read data from request and deserialize
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            return Response('ok')
        

@api_view()
def product_detail(request,id):
    product = get_object_or_404(Product,pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view()
def collection_detail(request,pk):
    return Response('ok')

