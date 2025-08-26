from django.contrib import admin
from .import models

## add decorator to register ProductAdmin in Model-Product class
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related =['collection']
    """
    Compute additional field in admin portal-
    Agenda: based on inventory return string 'Low' and 'OK'
    """
    # to implement sorting - add @admin.display
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
   
    def collection_title(self, product):
        """
        To display collection of product in admin portal-
        use select_related to reduce number of queries
        However,we have __str__ method in displaying collection,so we
        can use this method for other for other fields as well
        """
        return product.collection.title

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer','placed_at', 'payment_status']
    list_editable = ['payment_status']
    list_per_page = 10
    ordering = ['-placed_at']
    
# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # add computed column to display 'product_count 
    list_display = ['title', 'product_count']
    list_per_page = 10

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # we don't have product.count correct base qry
        return collection.product_set.count() 
    
    # modify base queryset by utilizing .annotate() & count()
    def get_queryset(self, request):
        product_count = super().get_queryset(request).\
            annotate(product_count=models.Count('product_set'))
        return product_count

  

  



# admin.site.register(models.OrderItem)

