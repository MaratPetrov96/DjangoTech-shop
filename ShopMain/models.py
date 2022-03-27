from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    title = models.CharField('title',max_length=100)
    translit = models.CharField('translit',max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Category'

    def __repr__(self):
        return self.title

    def __str__(self):
        return repr(self)

class Subcategory(models.Model):
    title = models.CharField('title',max_length=100)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,
                                 related_name='subs')
    translit = models.CharField('translit',max_length=100)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __repr__(self):
        return self.title

    def __str__(self):
        return repr(self)

class Item(models.Model):
    title = models.CharField('title',max_length=100)
    category = models.ForeignKey(Subcategory,on_delete=models.CASCADE
                                 ,related_name='items')
    picture = models.ImageField(upload_to='goods')
    price = models.FloatField()
    description = models.TextField()
    in_store = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='reviews')
    item = models.ForeignKey(Item,on_delete=models.CASCADE
                             ,related_name='reviews')
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])

class Busket(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    goods = models.ManyToManyField(Item,related_name='buyers')
    price = models.IntegerField(default=0)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE
                             ,related_name='orders')
    goods = models.ManyToManyField(Item,related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    price = models.FloatField(default=0.0)
