from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.core.mail import get_connection,send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import *
from .forms import *

def main(request): #главная страница
    return render(request,'main/main.html',{'user':request.user,'title':'DjangoTech - интернет-магазин бытовой техники',
                                            'categories':Category.objects.all()})

def about(request): # "О нас"
    return render(request,'main/about.html',{'user':request.user,'title':'DjangoTech - о нас'
                                             ,'categories':Category.objects.all()})

class ItemView(DetailView): #карточка товара
    model = Item
    template_name = 'main/item.html'
    context_object_name = 'one'
    reviews_per_page = 10
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['user'] = self.request.user
        try:
            self.kwargs['pg']
        except:
            self.kwargs['pg'] = 1
        context['reviews'] = Paginator(self.object.reviews.all(),self.reviews_per_page
                                       ).page(self.kwargs['pg'])
        context['user_review'] = False
        if self.request.user.is_authenticated:
            context['user_review'] = True
            try:
                self.object.reviews.get(user=self.request.user)
            except:
                context['range'] = range(5,0,-1)
                context['form_'] = ReviewForm()
        context['categories'] = Category.objects.all()
        return context

class SubcategoryView(DetailView): #подкатегория
    model = Subcategory
    template_name = 'main/Goods.html'
    context_object_name = 'one'
    reviews_per_page = 8
    def get_object(self):
        return Subcategory.objects.get(translit=self.kwargs['sub'])
    def get_context_data(self,**kwargs):
        try:
            self.kwargs['pg']
        except:
            self.kwargs['pg'] = 1
        context = super().get_context_data(**kwargs)
        context['title'] = f'Товары подкатегории {self.object.title}'
        context['categories'] = Category.objects.all()
        context['user'] = self.request.user
        context['data'] = self.object.items.all()
        context['search_'] = False
        context['one'] = self.object
        context['mn'] = min(context['data'].values_list('price',flat=True))
        context['mx'] = max(context['data'].values_list('price',flat=True))
        context['price'] = False
        try: #фильтрация по ценам
            context['min'] = self.kwargs['min_']
            context['max'] = self.kwargs['max_']
        except:
            context['min'] = context['mn']
            context['max'] = context['mx']
        try:
            context['data'] = context['data'].filter(price__range=(self.kwargs['min_'],self.kwargs['max_']))
            context['price'] = True
        except:
            pass
        try:
            context['data'] = Paginator(context['data'],self.reviews_per_page
                                    ).page(self.kwargs['pg'])
        except:
            pass
        return context

class BusketView(UserPassesTestMixin,DetailView): #корзина
    model = Busket
    template_name = 'main/Busket.html'
    context_object_name = 'busket'
    def test_func(self, **kwargs):
        self.kwargs['pk'] = self.request.user.pk
        return self.kwargs['pk']==self.get_object().user.pk
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        context['categories'] = Category.objects.all()
        context['user'] = self.request.user
        context['data'] = self.object.goods.all()
        return context

@login_required #добавление товара в корзину
def add(request,pk):
    if request.method == 'POST':
        busk = request.user.busket
        busk.goods.add(Item.objects.get(pk=pk))
        busk.price += Item.objects.get(pk=pk).price
        busk.save()
        return redirect('item',pk)

@login_required #форма платежа
def pay(request,summ):
    if request.method == 'POST':
        return render(request,'main/Pay.html',{'user':request.user,'categories':Category.objects.all(),'summ':summ,'title':'Платёж'})

@login_required #"оплата заказа")
def order(request):
    if request.method == 'POST':
        new = Order(user=request.user)
        new.save()
        new.goods.add(*request.user.busket.goods.all())
        new.price = sum(request.user.busket.goods.values_list('price',flat=True))
        new.save()
        message = f'Заказ № {new.pk}\n\n'
        message += '\n\n'.join(request.user.busket.goods.values_list('title',flat=True))
        message += f'\n\n{new.price}'
        message += f'\n\nID пользователя: {request.user.pk}'
        send_mail(f'Заказ № {new.pk}',
                  message,
                  settings.EMAIL_HOST_USER,
                  ['maratpython@yandex.ru'])
        bus = request.user.busket
        bus.goods.clear()
        bus.price = 0
        bus.save()
        return render(request,'main/Success.html',{'user':request.user,'categories':Category.objects.all()})

def search(request): #поиск
    if request.method === 'POST':
        return redirect('search',request.POST['query'])
#поиск сделан так чтобы можно было сохранить ссылку на его результаты

def search_res(request,query,pg=None,min_=None,max_=None): #результат поиска
    if not pg:
        pg = 1
    data = Item.objects.filter(
            Q(title__icontains=query) | Q(title__icontains=query.capitalize())
            )
    try:
        mn,mx = min(data.values_list('price',flat=True)),max(data.values_list('price',flat=True))
    except:
        return HttpResponse('Ничего не найдено')
    else:
        if min_ and max_:
            data = data.filter(price__range=(min_,max_))
        else:
            min_,max_ = min(data.values_list('price',flat=True)),max(data.values_list('price',flat=True))
        count = data.count()
        return render(request,'main/Goods.html',{'categories':Category.objects.all(),'data':Paginator(data,15).page(pg)
        ,'user':request.user,'search':True,'title':'Результаты поиска','query':query,'min':min_,
                                             'max':max_,'mn':mn,'mx':mx,'count_':count})

@login_required
def review(request,pk): #отзыв
    new = ReviewForm(request.POST)
    new = new.save(commit=False)
    new.user = request.user
    object_ = Item.objects.get(pk=pk)
    new.item = object_
    new.stars = request.POST['rate']
    new.save()
    return redirect('item',object_.pk)

@login_required #удаление из корзины
def delete_busket(request,pk):
    bus = request.user.busket
    bus.goods.remove(Item.objects.get(pk=pk))
    bus.price -= Item.objects.get(pk=pk).price
    bus.save()
    return redirect('busket')
