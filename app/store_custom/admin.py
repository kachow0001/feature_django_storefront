from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from store.models import Product
from store.admin import ProductAdmin
from tags.models import TaggedItem


# Register your models here.
## genric relation -content type using- InlineTabular option  Manage tags for Product
class TaggedInline(GenericTabularInline):
    autocomplete_fields =['tag']
    model = TaggedItem
    min_num =1
    max_num =10
    extra = 0

# create extension of ProductAdmin 
class CustomProductAdmin(ProductAdmin):
    inlines = [TaggedInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)

 