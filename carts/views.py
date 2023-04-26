from django.shortcuts import render,redirect
from store.models import Product
from carts.models import Cart,CartItem
# Create your views here.

def _get_cart_id(request):
    cart = request.session.session_key #get the sessionid
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)

    #check if cart exists then retrive otherwise create cart
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))

    #now add the product in cart

    try:
        #check if product is in CartItem then increment quantity
        cartItem = CartItem.objects.get(cart=cart,product=product)
        cartItem.quantity += 1
        cartItem.save()
    except:
        cartItem = CartItem.objects.create(cart=cart,product=product,quantity=1)
        cartItem.save()

    return redirect("cart")


def cart(request,cart_items=None):
    try:
        tax = 0
        grand_total=0
        sub_total=0
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
        cart_items = cart.cart_products.all()

        #calculate total price of products with quantity
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            grand_total += item.total_price
        
        tax = (grand_total * 20) / 100
        sub_total = grand_total + tax
    except Cart.DoesNotExist:
        pass #ignore
    context = {
        "cart_items":cart_items,
        "grand_total":grand_total,
        "tax":tax,
        "sub_total":sub_total,
    }
    return render(request,"store/cart.html",context)


def decrement_item(request,cart_item):
    item = CartItem.objects.get(id=cart_item)
    item.quantity -= 1
    item.save()
    if item.quantity == 0:
        item.delete()
    return redirect('cart')

def item_remove(request,cart_item):
    item = CartItem.objects.get(id=cart_item)
    item.delete()
    return redirect("cart")