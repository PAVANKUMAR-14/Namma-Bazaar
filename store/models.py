from django.db import models
from category.models import Category
from accounts.models import Accounts
from django.urls import reverse
from django.db.models import Avg,Count

# Create your models here.

class product (models.Model):
    product_name=models.CharField(max_length=200,unique=True)
    slug=models.SlugField(max_length=200,unique=True)
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    images=models.ImageField(upload_to='photos/products')
    stocks=models.IntegerField()
    is_available=models.BooleanField(default=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.product_name
    
    def get_url (self):
        return reverse ('product_detail', args=[self.category.slug,self.slug])
    
    def average_rating(self):
        reviews=ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg

    def review_count (self):
        review_count=ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count=0
        if review_count['count'] is not None:
            count=int(review_count['count'])
        return count

    
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color', is_active=  True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size', is_active=True)


variation_choices=(('color','color'),('size','size'))
class product_variation(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    variation_category=models.CharField( max_length=50,choices=variation_choices)
    variation_name=models.CharField(max_length=50)
    is_active=models.BooleanField(default=True)

    def __str__(self): 
        return self.variation_name
    
    objects=VariationManager()

class ReviewRating (models.Model):
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    user=models.ForeignKey(Accounts, on_delete=models.CASCADE)
    subject=models.CharField(max_length=50, blank=True)
    review=models.TextField(max_length=500, blank=True)
    rating=models.FloatField()
    IP= models.CharField(max_length=40, blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
    


class ProductGallery (models.Model):
    product=models.ForeignKey(product, on_delete=models.CASCADE)
    image=models.ImageField(upload_to='store/products',max_length=30)

    def __str__(self):
        return self.product.product_name

    


