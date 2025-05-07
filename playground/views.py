from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache import cache
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from django.views.decorators.cache import cache_page
from .tasks import notify_customers
import requests
# Create your views here.


class HelloView(APIView):
    @method_decorator(cache_page(5*60))
    def get(self, request):
        response = requests.get('https://httpbin.org/delay/2')
        data = response.json()
        return render(request, 'hello.html', {'name': data})
