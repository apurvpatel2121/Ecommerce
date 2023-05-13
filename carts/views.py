from django.shortcuts import render, redirect
from store.models import Product, Variation
from carts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
# Create your views here.


def _get_cart_id(request):
    cart = request.session.session_key  # get the sessionid
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    product = Product.objects.get(id=product_id)

    new_variation = []
    if request.method == "POST":
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                new_variation.append(variation)
            except:
                pass

    # check if cart exists then retrive otherwise create cart
    try:
        cart = Cart.objects.get(cart_id=_get_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product, user=user)
    else:
        cart_items = CartItem.objects.filter(product=product, cart=cart)

    existing_variation = []
    cartItem_id = []
    for cartItem in cart_items:
        # this will add multiple Variation objects of particular cartItem
        existing_variation.append(list(cartItem.variations.all()))
        cartItem_id.append(cartItem.id)
    print("Existing Var; ",existing_variation)
    print("new variations: ",new_variation)
    if (CartItem.objects.filter(product=product, cart=cart).exists() or CartItem.objects.filter(product=product, user=user).exists()) and new_variation in existing_variation:
        index = existing_variation.index(new_variation)
        if user is not None:
            cartItem = CartItem.objects.get(product=product,user=user,id=cartItem_id[index])
        else:
            cartItem = CartItem.objects.get(product=product,id=cartItem_id[index])
        cartItem.quantity += 1
    else:
        cartItem = CartItem.objects.create(user=user,cart=cart, product=product, quantity=1)
        cartItem.variations.add(*new_variation)

    cartItem.save()
    return redirect("cart")



#Cart Calculations
def cart_calculation(request):
    try:
        tax = 0
        grand_total = 0
        sub_total = 0

        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart)
        # calculate total price of products with quantity
        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            grand_total += item.total_price

        tax = (grand_total * 20) / 100
        sub_total = grand_total + tax
        context = {
        "cart_items": cart_items,
        "grand_total": grand_total,
        "tax": tax,
        "sub_total": sub_total,
    }
    except Cart.DoesNotExist:
        context = {}

    return context

def cart(request):
    context = cart_calculation(request)
    return render(request, "store/cart.html", context)


def decrement_item(request, cart_item):
    item = CartItem.objects.get(id=cart_item)
    if request.method == "POST":
        if request.user.is_authenticated and item.user == request.user:
            item.delete()
        else:
            if item.user is None and item.cart.cart_id == _get_cart_id(request):
                item.delete()
                
        return redirect("cart")
    else:
        if (request.user.is_authenticated and item.user == request.user) or (item.user is None and item.cart.cart_id == _get_cart_id(request)):
            item.quantity -= 1
            item.save()
            if item.quantity == 0:
                item.delete()
        return redirect('cart')


# def item_remove(request, cart_item):
#     item = CartItem.objects.get(id=cart_item)
#     item.delete()
#     return redirect("cart")


#checkout page
@login_required
def checkout(request):
    context = cart_calculation(request)
    return render(request,"store/checkout.html",context)