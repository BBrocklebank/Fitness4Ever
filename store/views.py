from django.shortcuts import render, get_object_or_404
from .models import Store

# Create your views here.

def all_products(request):
    ''' A view to show all products, including sorting and search queries '''

    products = Store.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'store/store.html', context)


def item_detail(request, product_id):
    ''' A view to show selected item details '''

    product = get_object_or_404(Store, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'store/item_detail.html', context)