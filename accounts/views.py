from django.shortcuts import render,redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView,UpdateView
from .models import *
from .forms import *
from core.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def my_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:user_list')
        else:
            messages.error(request,'username or password not correct')
            return redirect('accounts:login')
    else:

        return render(request, 'login.html')

@user_passes_test(lambda user: user.is_staff)
def register(request):
   if request.method == 'POST':
      form = UserRegisterForm(request.POST,request.FILES)

      if form.is_valid():
          form.save()
          msg = "Added "+ request.POST.get('first_name') + " " + request.POST.get('last_name') +" To  Clients "
          activity = Activities(user=request.user,title=msg)
          activity.save()

          return redirect('core:dashboard')
      else:
          messages.error(request, f'invalid details')

   else:
      form = UserRegisterForm()

   return render(request, 'register.html', {"form": form})

@user_passes_test(lambda user: user.is_staff)
def register2(request):
   if request.method == 'POST':
      form = UserRegisterForm(request.POST,request.FILES)

      if form.is_valid():
          instance = form.save(commit=False)
          instance.is_staff=True
          instance.save()
          msg = "Added "+request.POST.get('first_name') + " " + request.POST.get('last_name') + " To admin users "
          activity = Activities(user=request.user,title=msg)
          activity.save()

          return redirect('core:admin_list')
      else:
          messages.error(request, f'invalid details')

   else:
      form = UserRegisterForm()

   return render(request, 'register.html', {"form": form})
