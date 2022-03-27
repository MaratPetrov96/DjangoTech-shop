from django.shortcuts import render,HttpResponse,redirect
from ShopMain.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password1'])
            busket = Busket(user=User.objects.get(pk=user.pk))
            busket.save()
            return redirect('login')
    return render(request,'users/Register.html',{'form':UserCreationForm})

@login_required
def profile(request):
    data = request.user.orders.all()
    return render(request,'users/Profile.html',{'categories':Category.objects.all()
        ,'user':request.user,'title':'Личный кабинет'})
