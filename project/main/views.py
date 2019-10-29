from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import forms
from .models import Account, Textbook, Listing


def home(request):
    return HttpResponseRedirect(reverse('login'))

def login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('homepage'))
    if(request.method == 'POST'):
        # First get the username and password supplied
        username = request.POST.get("username")
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user);
            return HttpResponse("HELLO")
        else:
            pass
    return render(request, 'Login.html');

@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('homepage'))
    form = forms.AccountCreationForm();
    if(request.method == 'POST'):
        form = forms.AccountCreationForm(request.POST)
        if form.is_valid():
            if(Account.objects.filter(username=request.POST.get('username', None)).exists()):
                print("This account already exists");
            else:
                user = form.save()
                auth_login(request, user);
                return HttpResponseRedirect("HELLO")
        else:
            print("NOT VALID FORM")

    return render(request, 'Register.html',context={'form':form});
