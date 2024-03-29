from audioop import reverse
from itertools import product
from math import prod
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Store, Category
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def all_products(request):
    ''' A view to show all products, including sorting and search queries '''

    products = Store.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'Please enter something to search.')
                return redirect(reverse('store'))

            queries = Q(
                name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'store/store.html', context)


def item_detail(request, product_id):
    ''' A view to show selected item details '''

    product = get_object_or_404(Store, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'store/item_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'You do not have permission to access this area.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('item_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to add product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'store/add_products.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit item in the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'You do not have permission to access this area.')
        return redirect(reverse('home'))
    product = get_object_or_404(Store, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('item_detail', args=[product.id]))
        else:
            messages.error(request,
                           'Failed to update product. '
                           'Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'store/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request,
                       'You do not have permission to access this area.')
        return redirect(reverse('home'))
    product = get_object_or_404(Store, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('store'))
