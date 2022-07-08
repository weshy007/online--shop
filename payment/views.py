import braintree
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# Create your views here.
# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method == 'POST':
        #retrive nonce
        nonce = request.POST.get('payment_method_nonce', None)
        #create and sub,it gateway
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        # if result.method == 'POST':
        #     #retrive nonce
        #     nonce = request.POST.get('payment_method_nonce', None)
        #     #create and submit transaction
        #     result = gateway.transaction.sale({
        #         'amount': f'{total_cost:.2f}',
        #         'payment_method_nonce': nonce,
        #         'options': {
        #         'submit_for_settlement': True
        #         }
        #     })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            
            return redirect('payment:done')
        else:
            return redirect('payment:cancelled')
    
    else:
        #generate tokken
        client_token = gateway.client_token.generate()
        context = {
            'order': order,
            'client_token': client_token
        }
        return render(request, 'payment/process.html', context)


# payment has been successful
def payment_done(request):
    return render(request, 'payment/done.html')

# payment has been cancelled
def payment_canceled(request):
    return render(request, 'payment/canceled.html')