from django.db import models
from store.models import product,product_variation
from accounts.models import Accounts


# Create your models here.

class cart( models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    added_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
class cartItem(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    user=models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    variation=models.ManyToManyField(product_variation,blank=True)
    cart=models.ForeignKey(cart,on_delete=models.CASCADE, null=True)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    def __unicode__(self):
        return self.product
    
    def sub_total(self):
        return self.product.price * self.quantity
    



