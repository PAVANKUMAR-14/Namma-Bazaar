from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from carts.models import cartItem
from orders.models import Order,OrderProduct
from orders.forms import Order_form
from store.models import product
import datetime
import json
from orders.models import Payment
from django.core.mail import EmailMessage
from django.template.loader import render_to_string




# Create your views here

def payment (request):
    body=json.loads(request.body)
    print(body)
    order_total = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model

    payment=Payment(
        user=request.user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid= order_total.order_total,
        status=body['status']
        

    )
    payment.save()
    order_total.is_ordered=True
    order_total.payment=payment
    order_total.save()
    print('success')


    #Move the cart items to order_products model

    cart_items=cartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_product = OrderProduct.objects.create(
            order=order_total,  # Assign the order ForeignKey field
            user=request.user,
            payment=payment,
            product=item.product,
            # variations=item.variations.all() # Assuming variations are retrieved appropriately
            quantity=item.quantity,
            product_price=item.product.price,  # Assuming price is retrieved from the product
            ordered=True
        )
        order_product.save()

        cart_item=cartItem.objects.get(id=item.id)
        product_variation=cart_item.variation.all()
        order_products=OrderProduct.objects.get(id=order_product.id)
        order_products.variations.set(product_variation)
        order_products.save()

            #Reduce the sold products quantity in model

        products= product.objects.get(id=item.product.id)
        products.stocks -= item.quantity
        products.save()

    # clear the cart items
    cart_items.delete()

    #Sending email to user
    mail_subject='Thank you for ordering'
    message=render_to_string('order/order_received_email.html',{
                'user':request.user,
                'order':order_total,
            })
    to_mail=request.user.email
    send_mail=EmailMessage(mail_subject,message, to=[to_mail])
    send_mail.send()





    data={
        'order_number':order_total.order_number,
        'transID': payment.payment_id,
    }

    return JsonResponse(data)




        # order_product=OrderProduct()
        #  order_product.order_id=Order.id
        # order_product.payment=payment
        #  order_product.user_id=request.user.id
        #  order_product.product_id=item.product_id
        # order_product.product_price=item.product.price
        # order_product.quantity=item.quantity
        # order_product.ordered=True
        # order_product.save()






def place_order(request,total=0,quantity=0):
    current_user=request.user
    cart_items=cartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <=0 :
        return redirect ('store')
    tax=0
    grand_total=0
    for cart_item in cart_items:
        total=total + (cart_item.product.price * cart_item.quantity)
        quantity= quantity + cart_item.quantity
    tax= (3*total/100)
    grand_total= total+tax
    
    if request.method =='POST':
        form= Order_form (request.POST)
        if form.is_valid():
            #storing billing info inside the order table
            data= Order()
            data.user=current_user
            data.first_name=form.cleaned_data['first_name']
            data.last_name=form.cleaned_data['last_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line_1=form.cleaned_data['address_line_1']
            data.address_line_2=form.cleaned_data['address_line_2']
            data.city=form.cleaned_data['city']
            data.state=form.cleaned_data['state']
            data.country=form.cleaned_data['country']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()

            #Generating order number

            yr=int(datetime.date.today().strftime('%Y'))
            mt=int(datetime.date.today().strftime('%m'))
            dt=int(datetime.date.today().strftime('%d'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime('%Y%m%d') #20240323
            order_number=current_date + str(data.id)

            data.order_number=order_number
            data.save()

            order= Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context={
                'cart_items':cart_items,
                'order':order,
                'tax':tax,
                'order_total':grand_total,
                'total':total,
            }
            return render (request,'order/payments.html',context)
        else:
            return  redirect ('checkout')

def order_completion(request):
    order_number=request.GET.get('order_number')
    transID=request.GET.get('payment_id')
    try:
        order=Order.objects.get(order_number=order_number, is_ordered=True)
        order_product=OrderProduct.objects.filter(order_id=order.id)
        subtotal=0
        for i in order_product:
            subtotal= subtotal + i.product_price * i.quantity
        payment=Payment.objects.get(payment_id=transID)
        context={
        'order':order,
        'order_product':order_product,
        'order_number':order.order_number,
        'transID':payment.payment_id,
        'payment':payment,
        'subtotal':subtotal,

        }
    
        return render (request,'order/order_complete.html',context)
    except (Order.DoesNotExist,Payment.DoesNotExist):
        return redirect ('home')
    
    



            

