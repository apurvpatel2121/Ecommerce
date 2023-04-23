from django.shortcuts import render,redirect
from store.models import Product
from category.models import Category
# Create your views here.
def store(request,category_slug=None):
    products = Product.objects.all().filter(is_available=True)
    if category_slug is not None:
        try:
            category_obj = Category.objects.get(slug=category_slug)
            if category_obj:
                products = category_obj.category_products.all()
                print(products)
        except:
            return redirect('store')
    context = {
        'products':products,
        # 'product_count':products.count(), #directly in templeate using {{ products.count }}
        }

    return render(request,"store/store.html",context)


def product_detail(request,category_slug,product_slug):
    product = Product.objects.filter(slug=product_slug).first()
    context = {
        'product_detail':product,
    }
    return render(request,"store/product_detail.html",context)