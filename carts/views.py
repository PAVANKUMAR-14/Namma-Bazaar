from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import product,product_variation
from carts.models import cart,cartItem
# Create your views here.


def _cart_id(request):
    session_id = request.session.session_key
    if not session_id:
        session_id = request.session.create()
      # Assign the newly created session key
    return session_id



def add_cart (request,product_id):
    products=product.objects.get(id=product_id)
    current_user=request.user
    #if the user is authenticated
    if current_user.is_authenticated:
            product_variations=[]
            if request.method=='POST':
                for items in request.POST:
                    key=items
                    value=request.POST[key]
                    try:
                        variation_list=product_variation.objects.get(product=products, variation_category__iexact=key, variation_name__iexact=value)
                        product_variations.append(variation_list)
                    except:
                        pass


            is_cart_item_exists= cartItem.objects.filter(product=products,user=current_user).exists()
            if is_cart_item_exists:
                cart_item=cartItem.objects.filter(product=products, user=current_user)
                #need 1. existing variations 2. product variation(want to add) 3.item_id
                ex_var_list=[]
                id=[]
                for item in cart_item:
                    existing_variation=item.variation.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

                if product_variations in ex_var_list:
                    index=ex_var_list.index(product_variations)
                    item_id=id[index]
                    item=cartItem.objects.get(product=products, id=item_id)
                    item.quantity = item.quantity + 1 
                    item.save()
                        # increase quantity
                else:
                    item=cartItem.objects.create(product=products, user=current_user, quantity=1)
                    if len(product_variations) > 0 :
                        item.variation.clear()
                        item.variation.add(*product_variations)
                    item.save()

            else :
                cart_item=cartItem.objects.create(
                    product=products,
                    user=current_user,
                    quantity=1,
                )
                if len(product_variations) > 0 :
                    cart_item.variation.clear()
                    cart_item.variation.add(*product_variations)
                cart_item.save()
            return redirect ('cart_page')
    
    #  If the user is not authenticated   
    else:
        product_variations=[]
        if request.method=='POST':
            for items in request.POST:
                key=items
                value=request.POST[key]
                try:
                    variation_list=product_variation.objects.get(product=products, variation_category__iexact=key, variation_name__iexact=value)
                    product_variations.append(variation_list)
                except:
                    pass

        try:
            Cart=cart.objects.get(cart_id=_cart_id(request))
        except cart.DoesNotExist:
            Cart=cart.objects.create(
                cart_id=_cart_id(request)
            )
            Cart.save()



        is_cart_item_exists= cartItem.objects.filter(product=products,cart=Cart).exists()
        if is_cart_item_exists:
            cart_item=cartItem.objects.filter(product=products, cart=Cart)
            #need 1. existing variations 2. product variation(want to add) 3.item_id
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variations in ex_var_list:
                index=ex_var_list.index(product_variations)
                item_id=id[index]
                item=cartItem.objects.get(product=products, id=item_id)
                item.quantity = item.quantity + 1 
                item.save()
                    # increase quantity
            else:
                item=cartItem.objects.create(product=products, cart=Cart, quantity=1)
                if len(product_variations) > 0 :
                    item.variation.clear()
                    item.variation.add(*product_variations)
                item.save()

        else :
            cart_item=cartItem.objects.create(
                product=products,
                cart=Cart,
                quantity=1,
            )
            if len(product_variations) > 0 :
                cart_item.variation.clear()
                cart_item.variation.add(*product_variations)
            cart_item.save()
        return redirect ('cart_page')

def remove_cart(request,product_id,cart_item_id ):
    products=get_object_or_404(product,id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item=cartItem.objects.get(user=request.user,product=products, id=cart_item_id)
        else:
            Cart=cart.objects.get(cart_id=_cart_id(request))
            cart_item=cartItem.objects.get(cart=Cart,product=products, id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity -=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect ('cart_page')


def remove_cart_item (request,product_id,cart_item_id):
    products=get_object_or_404(product,id=product_id)
    if request.user.is_authenticated:
        cart_item=cartItem.objects.get(user=request.user,product=products,id=cart_item_id)
    else:
        Cart=cart.objects.get(cart_id=_cart_id(request))
        cart_item=cartItem.objects.get(cart=Cart,product=products,id=cart_item_id)
    cart_item.delete()
    return redirect('cart_page')

    

def cart_page (request,total=0,quantity=0,cart_item=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_item=cartItem.objects.filter(user=request.user, is_active=True)
        else:
            Cart=cart.objects.get(cart_id=_cart_id(request))
            cart_item=cartItem.objects.filter(cart=Cart,is_active=True)
        for cart_items in cart_item:
            total=total + (cart_items.product.price * cart_items.quantity)
            quantity= quantity + cart_items.quantity
        tax= (3*total/100)
        grand_total=total+tax
        
    except :
        pass

    context={
        'cart_items':cart_item,
        'quantity':quantity,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render (request,'store/cart.html',context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_item=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_item=cartItem.objects.filter(user=request.user, is_active=True)
        else:
            Cart=cart.objects.get(cart_id=_cart_id(request))
            cart_item=cartItem.objects.filter(cart=Cart,is_active=True)
        for cart_items in cart_item:
            total=total + (cart_items.product.price * cart_items.quantity)
            quantity= quantity + cart_items.quantity
        tax= (3*total/100)
        grand_total=total+tax
        
    except :
        pass

    context={
        'cart_items':cart_item,
        'quantity':quantity,
        'total':total,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render (request,'store/checkout.html',context)