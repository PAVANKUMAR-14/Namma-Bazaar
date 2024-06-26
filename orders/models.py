from django.db import models
from accounts.models import Accounts
from store.models import product,product_variation

# Create your models here
class Payment(models.Model):
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=50)
    payment_method=models.CharField(max_length=50)
    amount_paid=models.CharField(max_length=50)
    status=models.CharField(max_length=50)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order (models.Model):

    STATUS=(
            ('New','New'),
            ('Accepted','Accepted'),
            ('Completed','Completed'),
            ('Cancelled','Cancelled'),
            )
    
    user=models.ForeignKey(Accounts,on_delete=models.SET_NULL, null=True)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True )
    order_number=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField()
    address_line_1=models.CharField(max_length=50)
    address_line_2=models.CharField(max_length=50, blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.CharField(max_length=200, blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=50, choices=STATUS,default='New')
    ip=models.CharField(max_length=50, blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def full_address(self):
        return f'{self.address_line_1}{self.address_line_2}'


    def __str__(self):
        return self.first_name


class OrderProduct (models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    user=models.ForeignKey(Accounts,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment, on_delete=models.SET_NULL,null=True, blank=True )
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    variations=models.ManyToManyField(product_variation,blank=True)
    quantity=models.IntegerField()
    product_price=models.FloatField()
    ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name
    
                            