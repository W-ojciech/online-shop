from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Category name')
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name
    def __int__(self):
        return self.id



class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    added_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)






class ProductInBasket(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    basket_id = models.ForeignKey('Basket', on_delete=models.DO_NOTHING)
    volume_of_product = models.IntegerField(default=0)


class Basket(models.Model):
    quantity = models.IntegerField(default=0)
    customers = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through=ProductInBasket)

    def remove_product(self, product):
        product_in_basket = ProductInBasket.objects.get(basket_id=self, product_id=product)
        if product_in_basket.volume_of_product > 1:
            product_in_basket.volume_of_product -= 1
            product_in_basket.save()
        else:
            product_in_basket.delete()

    def add_product(self, product):
        product_in_basket, created = ProductInBasket.objects.get_or_create(basket_id=self,
                                                                  product_id=product)
        if created:
            product_in_basket.volume_of_product = 1
        else:
            product_in_basket.volume_of_product+=1
        product_in_basket.save()



class Comment(models.Model):
    text = models.TextField(max_length=1024)
    added_date = models.DateField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)



class Page(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=256)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)
