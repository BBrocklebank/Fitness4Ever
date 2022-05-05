from django.shortcuts import render
from .models import Store

# Create your views here.

def all_products(request):
    ''' A view to show all products, including sorting and search queries '''

    products = Store.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'store/store.html', context)
