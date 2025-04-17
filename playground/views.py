from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product, OrderItem, Order, Collection

# Create your views here.


def say_hello(request):

    return render(request, 'hello.html', {'name': 'Rodrigo'})
