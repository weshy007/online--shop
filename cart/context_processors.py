from .cart import Cart

def cart(request):
    return {'cart': cart(request)}