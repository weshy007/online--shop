from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm

from .models import Category, Product

# Create your views here.
# display the product catalog
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'products': products,
        'category': category,
        'categories': categories
    }

    return render(request, 'shop/product/list.html', context)


# display the selected product's detail 
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()

    context = { 
        'product': product,
        'cart_product_form': cart_product_form
    }

    return render(request, 'shop/product/detail.html', context)
