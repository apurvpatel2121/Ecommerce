from django.urls import path
from carts import views

urlpatterns = [
    path("",views.cart,name="cart"),
    path("add_cart/<int:product_id>/",views.add_cart,name="add_cart"),
    path("decrement_item/<int:cart_item>/",views.decrement_item,name="decrement_item"),
    path("item_remove/<int:cart_item>/",views.item_remove,name="item_remove"),
]