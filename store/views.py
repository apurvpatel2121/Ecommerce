from django.shortcuts import render, redirect
from store.models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _get_cart_id
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


def store(request, category_slug=None):
    products = Product.objects.all().filter(is_available=True).order_by('id')
    products_by_page = 6
    if category_slug is not None:
        try:
            category_obj = Category.objects.get(slug=category_slug)
            if category_obj:
                products = category_obj.category_products.all().order_by("id")
                products_by_page = 2
        except:
            return redirect('store')
        

    paginator = Paginator(products,products_by_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'product_count':products.count()
    }

    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    product = Product.objects.filter(slug=product_slug).first()
    context = {}

    # get the cart_id from session
    cart_id = _get_cart_id(request)
    product_in_user_cart = CartItem.objects.filter(
        cart__cart_id=cart_id, product=product).exists()

    context.update({
        'product_detail': product,
        # 'product_in_user_cart': product_in_user_cart,
    })
    return render(request, "store/product_detail.html", context)

def search(request):
    keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.order_by("-created_date").filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
    context = {
        "products":products,
        "product_count":products.count(),
    }
    return render(request,"store/store.html",context)