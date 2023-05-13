from category.models import Category
from carts.models import Cart,CartItem
from carts.views import _get_cart_id
def menu_list(request):
    categories = Category.objects.all().order_by("category_name")
    return dict(categories=categories)


def total_cart_items(request):
    total_cart_items = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart_items = CartItem.objects.filter(cart__cart_id=_get_cart_id(request))
        for cart_item in cart_items:
            total_cart_items += cart_item.quantity

    except Cart.DoesNotExist:
        pass
    return dict(total_cart_items=total_cart_items)