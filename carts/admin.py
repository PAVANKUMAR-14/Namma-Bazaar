from django.contrib import admin
from .models import cart,cartItem

# Register your models here.


class cartAdmin(admin.ModelAdmin):
    list_display=['cart_id','added_date']

class cartItemAdmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']

    
admin.site.register(cart, cartAdmin)
admin.site.register(cartItem, cartItemAdmin)
