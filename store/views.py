from audioop import reverse
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Store, Category

# Create your views here.

def all_products(request):
    ''' A view to show all products, including sorting and search queries '''

    products = Store.objects.all()
    query = None
    categories = None

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter something to search.')
                return redirect(reverse('store'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'store/store.html', context)


def item_detail(request, product_id):
    ''' A view to show selected item details '''

    product = get_object_or_404(Store, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'store/item_detail.html', context)