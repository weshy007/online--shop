from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product

from coupons.forms import CouponApplyForm
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
'''
This is the view for adding products to the cart or updating quantities 
for existing products.
'''
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )

    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect ('cart:cart_detail')


'''
View to display the cart and its items
'''
def cart_detail(request):
    cart = Cart(request)
    
    #Update cart quantity 
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                    initial={'quantity': item['quantity'],
                                    'override': True
                                    })
                                    
    coupon_apply_form = CouponApplyForm()

    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form
    }
                                                    
    return render(request, 'detail.html', context)