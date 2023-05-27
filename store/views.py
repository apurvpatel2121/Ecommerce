from django.shortcuts import render, redirect
from store.models import Product
from category.models import Category
from carts.models import Cart, CartItem
from carts.views import _get_cart_id
from django.core.paginator import Paginator
from django.db.models import Q,Avg,Count
from orders.models import OrderProduct
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

    orderproduct = False
    if request.user.is_authenticated:
        orderproduct = OrderProduct.objects.filter(user=request.user, product_id=product.id).exists()

    reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    avg_review = reviews.aggregate(average_review=Avg("rating"))
    total_review = reviews.aggregate(total_reviews=Count("id"))

    context.update({
        'product_detail': product,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'avg_review': avg_review['average_review'],
        'total_review': total_review['total_reviews'],
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

from store.models import ReviewRating
from store.forms import ReviewForm
from django.contrib import messages
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)