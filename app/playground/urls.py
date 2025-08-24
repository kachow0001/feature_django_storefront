from django.urls import path
from . import views

# URLConfig module = include in main url config module

urlpatterns = [
    path('hello/', views.greetings)
]
