from django.urls import path, include
from .import views 
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
#register viewsets with router(with 'prefix' and 'viewset class')
router.register('products',views.ProductViewSet)
router.register('collections',views.CollectionViewSet)

urlpatterns = router.urls

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
#     path('collections/',views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),

# ]
