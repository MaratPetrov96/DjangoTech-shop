from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Item)
#admin.site.register(Busket)
#admin.site.register(Order)

class BusketGoods(admin.TabularInline):
    model = Busket.goods.through

class Ordered(admin.TabularInline):
    model = Order.goods.through

@admin.register(Busket)
class BusketAdmin(admin.ModelAdmin):
    inlines = (BusketGoods,)
    exclude = ('goods',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (Ordered,)
    exclude = ('goods',)
