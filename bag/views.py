from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    ''' View, returns shopping bag page '''
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add specified quantity of item to bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    #Checks for bag session variable, initialises one if not found (python dictionary)
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)