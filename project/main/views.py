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

@login_required
def homepage(request):
    listings = Listing.objects.all();
    return render(request, 'Homepage.html',context={'listings':listings})

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
            return HttpResponseRedirect(reverse('homepage'))
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
                return HttpResponseRedirect(reverse('homepage'))
        else:
            print("NOT VALID FORM")

    return render(request, 'Register.html',context={'form':form});


@login_required
def my_profile(request):
    return render(request, 'Profile.html');

@login_required
def settings(request):
    data = {'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name,}
    form = forms.AccountChangeForm(initial=data)
    if request.method == 'POST':
        form = forms.AccountChangeForm(request.POST)
        if(form.is_valid()):
            modified_data = {};
            if request.user.check_password(request.POST.get('password')):
                pass;
            else:
                request.user.set_password(request.POST.get('password'))
                user = request.user.save();
                auth_login(request, user);
            if request.FILES.get('Profile_Picture') is not None:
                request.user.Profile_Picture = request.FILES.get('Profile_Picture');
            if request.user.email != request.POST.get('email') and request.POST.get('email') != '':
                request.user.email = request.POST.get('email')
            if request.user.first_name != request.POST.get('first_name') and request.POST.get('first_name') != '':
                request.user.first_name = request.POST.get('first_name')
            if request.user.last_name != request.POST.get('last_name') and request.POST.get('last_name') != '':
                request.user.last_name = request.POST.get('last_name')

            modified_data['email'] = request.POST.get('email')
            modified_data['first_name'] = request.POST.get('first_name')
            modified_data['last_name'] = request.POST.get('last_name')
            request.user.save()
            new_form = forms.AccountChangeForm(initial=modified_data)
            return render(request, 'Settings.html', context={'form': new_form})
        else:
            print(form.errors)
    return render(request, 'Settings.html',context={'form':form});


@login_required
def product_page(request, textbook_id):
    textbook = get_object_or_404(Textbook, pk=textbook_id);
    listing = Listing.objects.filter(Textbook=textbook).first()
    return render(request, 'Product_Page.html', context={'listing': listing})

@login_required
def view_profile(request, account_username):
    account = Account.objects.filter(username=account_username).first()
    return render(request, 'Other_Users_Profile.html', context={'account':account})
