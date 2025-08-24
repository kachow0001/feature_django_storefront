from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


# Create your views here.
def greetings(request):
    query_set = Product.objects.all()

    for items in query_set:
        print(items)

    return render(request, 'hello.html',
                  {'name': 'K'})
