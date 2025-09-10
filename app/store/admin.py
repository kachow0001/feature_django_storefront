from django.contrib import admin,messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import Count
from django.urls import reverse 
from django.utils.html import format_html,urlencode
from .import models

# creating cutome filter - adding Inventory
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory' # pick this name in url query

    # define lookups method - return list of tuples
    def lookups(self,request,model_admin):
        return [
            ('<10','Low')
        ]
    # define queryset method - filter logic 
    def queryset(self,request,queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # adding auto-complete search field for collection in "add Product form"
    autocomplete_fields = ['collection']
    # adding pre-polulated option for slug field based on tittle field - "add Product form""
    prepopulated_fields = {
        'slug':['title']
    }
    
    actions = ['clear_inventory']
 
    list_display = ['title', 'unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related =['collection']
    list_filter = ['collection','last_update',InventoryFilter]
    search_fields = ['title']

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
    
    ## adding function for custom action
    @admin.action(description='Clear Inventory')
    # description here text that appears in dropdown
    def clear_inventory(self,request,queryset): 
        #here queryset is the selected rows/values in admin portal
        updated_count= queryset.update(inventory=0)
        self.message_user(request,
                          f"{updated_count}product were successfully updated.",
                          messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership','order_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering =['first_name','last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    ## add new field - computing customer count for order
    @admin.display(ordering='order_count', description='Orders')
    def order_count(self, customer):
        return customer.order_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )
# editing child using Inline for Managing OrderItem in Order  

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    max_num = 10
    extra = 0
    #to avoid extra empty forms

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields =['customer']
    inlines = [OrderItemInline]
    list_display = ['id','customer','placed_at']
    list_per_page = 10
    ordering = ['-placed_at']
    
# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    # add computed column to display 'product_count 
    list_display = ['title', 'product_count']
    # add search -field (auto-completefield) search 
    # -collection in "add product form"
    search_fields = ['title']

    @admin.display(ordering='product_count')
    def product_count(self, collection):
        # implement reverse-url to capture dynamic url from target model and target list page (product)
        # reverse('admin:store_model_page')
        url = (reverse('admin:store_product_changelist')
               + '?' +
               urlencode({'collection__id': str(collection.id)})
               )
        return format_html("<a href = '{}'>{}</a>", url, collection.product_count)

    # modify base queryset by utilizing .annotate() & count()
    def get_queryset(self, request):
        return super().get_queryset(request).\
           annotate(product_count=Count('products'))

# admin.site.register(models.OrderItem)

