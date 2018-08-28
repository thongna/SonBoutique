from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from account.models import Profile
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

# Create your views here.
def order_create(request):
    cart = Cart(request)
    payment_method = request.POST.get('payment_method')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.total_price = cart.get_total_price_after_discount()
            order.pay_by = payment_method
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            return render(request,
                              'orders/order/created.html',
                              {'order': order})
    else:
        data = {}
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            data = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 'address': profile.address, 'email': request.user.email, 'phone_number': profile.phone_number}
        form = OrderCreateForm(initial=data)

    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form,})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/detail.html', {'order': order})