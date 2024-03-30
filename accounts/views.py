from django.shortcuts import render,redirect, get_object_or_404
from accounts.forms import RegistrationForm, UserForm, UserProfileForm
from accounts.models import Accounts, UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.models import cart,cartItem
from carts.views import _cart_id
import requests
from orders.models import Order,OrderProduct

# For email verification code
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            username=email.split('@')[0]
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            user= Accounts.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()
            #Email verification
            current_site=get_current_site(request)
            mail_subject='Please verify your account'
            message=render_to_string('accounts/account_verification_mail.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_mail=email
            send_mail=EmailMessage(mail_subject,message, to=[to_mail])
            send_mail.send()
            # messages.success(request, 'Successfully registered, please check your mail')
            return redirect('/account/login/?command=verification&email='+email)    
    else:
        form=RegistrationForm()
    context={'form':form}

    return render (request, 'accounts/register.html',context)

def Login(request):
    if request.method =='POST':
        email=request.POST['Email']
        password=request.POST['Password']
        print(email, password)
        user=authenticate(email=email, password=password)
        # print(user)
        if user is not None :
            try:
                Cart=cart.objects.get(cart_id=_cart_id(request))
                is_cartitem_exists=cartItem.objects.filter(cart=Cart).exists()
                if is_cartitem_exists:
                    cart_items=cartItem.objects.filter(cart=Cart)

                    #getting  product variation by cart_id
                    product_variation=[]
                    for item in cart_items:
                        variation=item.variation.all()
                        product_variation.append(list(variation))

                    # got the cart item from the user to access product variations
                    cart_item=cartItem.objects.filter( user=user)
                    ex_var_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variation.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)


                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id=id[index]
                            item=cartItem.objects.get(id=item_id)
                            item.quantity = item.quantity + 1 
                            item.user=user
                            item.save()
                        else:
                            cart_items=cartItem.objects.filter(cart=Cart)
                            for item in cart_items:
                                item.user=user
                                item.save()
            except:
                pass

            login(request,user)
            messages.success(request,'You are sucessfully logged in, will be redirected to dashboard')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                print('query:', query)
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
            except:
                return redirect ('dashboard')

        else:
            messages.error(request,'Invalid login credential')
            return redirect ('login')
    return render (request, 'accounts/login.html')

@login_required(login_url='login')
def Logout (request):
    logout(request)
    messages.success(request,'You are logged out')
    return redirect ('login')

def activate (request, uidb64, token):
    try:

        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)

    except (TypeError,ValueError, Accounts.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request,'You are verified successfully')
        return redirect ('login')
    else:
        messages.warning(request,'failed to verify')
        return redirect('register')

@login_required  
def dashboard (request):
    orders=Order.objects.filter(user_id=request.user.id, is_ordered=True).order_by('-created_at')
    orders_count= orders.count()
    userprofile=UserProfile.objects.get(user_id=request.user.id)
    context={ 'orders_count':orders_count, 'userprofile':userprofile}
    return render(request,'accounts/dashboard.html', context)


def forgetPassword (request):
    if request.method=='POST':
        email=request.POST['Email']
        if Accounts.objects.filter(email=email).exists():
            user=Accounts.objects.get(email__exact=email)
            #Email verification
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_mail=email
            send_mail=EmailMessage(mail_subject,message, to=[to_mail])
            send_mail.send()
            messages.success(request,'Reset password link has been sent to your email')
            return redirect ('login')
        else:
            messages.warning(request,'Account does not exist')

            return redirect('forgetPassword')

    return render(request,'accounts/forgetPassword.html')


def resetpassword_validate(request,uidb64,token):
    try:

        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)

    except (TypeError,ValueError, Accounts.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect ('resetPassword')
    else:
        messages.warning(request,'This link is expired')
        return redirect ('login')

def resetPassword (request):
    if request.method =='POST':
        password=request.POST['password']
        confirm_password=request.POST['ConfirmPassword']
        if password== confirm_password:
            uid=request.session.get('uid')
            user=Accounts.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password reset successful')
            return redirect('login')

        else:
            messages.warning(request,'Password does not match')
            return redirect ('resetPassword')
    else:
        return render(request,'accounts/resetpassword.html')




def my_orders(request):
    orders=Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context={'orders': orders}
    return render(request,'accounts/my_orders.html', context)

@login_required(login_url='login')
def edit_profile (request):
    userprofile=get_object_or_404(UserProfile, user=request.user)
    if request.method=='POST':
        userform=UserForm(request.POST, instance= request.user)
        userprofileform=UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if userform.is_valid() and userprofileform.is_valid():
            userform.save()
            userprofile.save()
            messages.success(request,'Your profile has been updated')
            return redirect('edit_profile')
    else:
        userform=UserForm(instance=request.user)
        userprofileform=UserProfileForm(instance=userprofile)

    context={
        'userform':userform,
        'userprofileform':userprofileform,
        'userprofile':userprofile,
    }

    return render (request, 'accounts/edit_profile.html',context)

@login_required(login_url='login')
def change_password(request):
    if request.method=='POST':
        current_password=request.POST['current_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        user=Accounts.objects.get(username__exact=request.user.username)

        if new_password==confirm_password:
            check=user.check_password(current_password)
            if check:
                user.set_password(new_password)
                user.save()
                # logout(request) IT WILL AUTOMATICALLY LOGOUT 
                messages.success(request,'Your password updated sucessfully')
                # return redirect ('dashboard')
            else:
                messages.warning(request,'Please ensure that your current password are entered correctly')
                return redirect ('change_password')
        else:
            messages.warning(request, 'Please ensure that your new password and confirm password are entered correctly')
            return redirect ('change_password')

    return render (request, 'accounts/change_password.html')


def  order_detail (request, order_id):
    order_detail=OrderProduct.objects.filter(order__order_number= order_id)
    order=Order.objects.get(order_number=order_id) 
    subtotal=0

    for i in order_detail:
        subtotal+= i.product_price * i.quantity

    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal
    }


    return render (request, 'accounts/order_detail.html', context)











    

