from carts.models import cart,cartItem
from carts.views import _cart_id

def cart_count(request):
    cart_counts=0

    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items= cartItem.objects.all().filter(user=request.user)
            else:
                Cart=cart.objects.get(cart_id=_cart_id(request))
                cart_items=cartItem.objects.all().filter(cart=Cart)

            for cart_item in cart_items :
                cart_counts += cart_item.quantity
        except cart.DoesNotExist:
            cart_counts=0

    return dict(cart_counts=cart_counts)
