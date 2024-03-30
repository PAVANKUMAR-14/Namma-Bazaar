from django.contrib import admin
from store.models import product,product_variation, ReviewRating,ProductGallery
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline (admin.TabularInline):
    model=ProductGallery
    extra=1



class ProductAdmin (admin.ModelAdmin):
    list_display=['product_name','price','stocks','category','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)}
    inlines=[ProductGalleryInline]

admin.site.register(product,ProductAdmin)


class VariationAdmin(admin.ModelAdmin):
    list_display=['product','variation_category','variation_name','is_active']
    list_filter=['product','variation_category','variation_name','is_active']
    list_editable=('is_active',)


admin.site.register(product_variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)

    



