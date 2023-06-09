from django.shortcuts import render,redirect
from carts.models import CartItem
from orders.models import Order,Payment,OrderProduct
from django.http import JsonResponse
from orders.forms import OrderForm
# Create your views here.
import datetime
import json
def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(order_number=body['orderID'])

    payment = Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid = order.order_total,
        status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    #savig cart items to orderProduct table 
    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        orderProduct = OrderProduct()
        orderProduct.order_id = order.id
        orderProduct.payment = payment
        orderProduct.user_id = request.user.id
        orderProduct.product_id = item.product_id
        orderProduct.quantity = item.quantity
        orderProduct.product_price = item.product.price
        orderProduct.orderd = True
        orderProduct.save()
        for variation in item.variations.all():
            orderProduct.variation.add(variation)

        #reduce the quantity of products in stock
        #reduce()

    #send order received email to customer
    # email.send()

    #delete cart items
    # cart_items.delete()
    data = {
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }

    return JsonResponse(data)


def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.count() <= 0:
        return redirect("store")
    # quantity = 0
    total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        # quantity += cart_item.quantity

    tax = (total * 20) / 100

    user = request.user
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            
            data = Order()
            data.user_id = request.user.id
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']

            data.tax = tax
            data.order_total = total + tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() #we need full id while saving order_number field / so without saving object id will be none at last (i.e. 20230519None)

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime('%Y%m%d')
            order_number = current_date + str(data.id) # 20230519+01
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(order_number=order_number)

            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':total+tax,
            }

            return render(request,'orders/payments.html',context)
        
    return redirect("/")



def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number,is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity
        payment = Payment.objects.get(payment_id=transID)

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'payment': payment,
            'subtotal': sub_total,
        }
        return render(request, 'orders/order_complete.html', context)
    except:
        return redirect("home")
