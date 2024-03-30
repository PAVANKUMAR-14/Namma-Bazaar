from django.contrib import admin
from orders.models import Payment,Order,OrderProduct

# Register your models here.

class OrderProductInline (admin.TabularInline):
    model=OrderProduct
    extra=0
    readonly_fields=['payment','user','quantity','product','product_price','ordered']







class orderAdmin (admin.ModelAdmin):
    list_display=['order_number','full_name','email','phone','order_total','tax','city','is_ordered','status']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','email','phone']
    list_per_page=20
    inlines=[OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order,orderAdmin)
admin.site.register(OrderProduct)
