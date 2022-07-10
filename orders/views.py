from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, 
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'])

            # clear the cart after
            cart.clear()

            # launch asynchronous task withn celery task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()

    context = {
        'cart': cart, 
        'form': form
    }

    return render(request, 'create.html', context) 


# Extending the administration site with a custom view
@staff_member_required
def admin_order_detail(request, order_id):
    order =  get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

