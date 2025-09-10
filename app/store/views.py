from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from .models import Product,Collection
from .serializers import ProductSerializer,CollectionSerializer

"""# function based views here.
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
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        """
# # creating class based view - using generics
# class ProductList(ListCreateAPIView):

#     # def get(self,request):
#     #     queryset = Product.objects.select_related('collection').all()  # ORM

#     # def get_serializer_class(self):
#     #     return ProductSerializer

#     # def get_serializer_context(self, request):
#     #         return {'request': self.request}
#     #Instead of defining above methods we can use below  attributes

#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer

#     def get_serializer_context(self):
#         return {'request': self.request}


# class ProductDetail(RetrieveUpdateDestroyAPIView):

#     # def get(self,request,pk):
#     #     product = get_object_or_404(Product.objects.select_related('collection'), id=pk)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)

#     # def put(self,request,pk):
#     #     product = get_object_or_404(Product.objects.select_related('collection'), id=pk)
#     #     serializer = ProductSerializer(product,data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data,status=status.HTTP_200_OK)
#     #Instead of defining above methods we can use below  attributes

#     queryset = Product.objects.select_related('collection')
#     serializer_class = ProductSerializer

#     def delete(self,request,pk):
#         product = get_object_or_404(Product.objects.select_related('collection'), id=pk)
#         if product.order_items.count() > 0:
#             return Response({'error':'Product cannot be deleted because it is associated with an order item.'},status=status.HTTP_400_BAD_REQUEST)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# combining command code from both ProductList and ProductDetail using Viewsets()

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # def delete(self,request,pk):
    #     product = get_object_or_404(Product.objects.select_related('collection'), id=pk)
    #     if product.order_items.count() > 0:
    #         return Response({'error':'Product cannot be deleted because it is associated with an order item.'},status=status.HTTP_400_BAD_REQUEST)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# overriding destroy method of ModelViewSet to add custom delete logic
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return{'request':self}
        
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)

# class CollectionDetail(RetrieveUpdateDestroyAPIView):

#     queryset = Collection.objects.annotate(products_count=Count('products')).all()
#     serializer_class = CollectionSerializer

    # def delete(self,request,pk):
    #     collection = get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
