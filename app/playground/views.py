from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Customer,Collection,Order,OrderItem
from tags.models import TaggedItem


# Create your views here.
def greetings(request):
   query_set = Product.objects.filter(unit_price__range=(20,30))
   #query_set_cus_res= Customer.objects.filter(email__icontains='.com')

   ## ContentType- used Decoupling Tags app and store app,utilizing
   ## inbuilt Managers -> contenttype and obj_id

   # content_type = ContentType.objects.get_for_id('Product')
   # queryset_tags = TaggedItem.objects.select_related('tags').\
   #    filter(content_type = content_type,
   #          object_id = 1
   #          )

   ## use Custom Managers -> obj_id and Obj_type
   # queryset_tags = TaggedItem.objects.get_tags_for(Product, 1)

   # ## Updating and Creating rec in db 
   # collection  = Collection()
   # collection.title = 'Video Games'
   # collection.featured_product = Product(pk=1)
   # collection.save()

   ## transactions queries using context-managers - build qry to creating order rec for items 
   # first create order and create orderItem 

   # with transaction.atomic():

   #    order = Order()
   #    order.customer_id = 1
   #    order.save()

   #    item = OrderItem()
   #    item.order = order
   #    item.product_id = 1
   #    item.quantity = 1
   #    item.unit_price = 10
   #    item.save()


   return render(request, 'hello.html',
                  {'name': 'K','products':list(query_set)})