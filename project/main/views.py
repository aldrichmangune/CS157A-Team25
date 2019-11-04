from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from . import forms
from .models import Account, Textbook, Listing


def home(request):
    return HttpResponseRedirect(reverse('login'))

@login_required
def homepage(request):
    listings = Listing.objects.raw("Select * from Listing");
    return render(request, 'Homepage.html',context={'listings':listings})

def login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'Login.html');

@require_POST
@csrf_exempt
def login_request(request):
    if request.is_ajax() == True:
        context = {}
        username = request.POST.get("username")
        password = request.POST.get("password")
        if len(Account.objects.raw("SELECT * FROM Account WHERE username = %s", [username])) == 0:
            context['username'] = 'Not found'
            context['password'] = 'Not found'
        else:
            context['username'] = 'Found'
            user = authenticate(username=username, password=password)
            if user is None:
                context['password'] = 'Incorrect'
            else:
                auth_login(request, user)
                context['message'] = 'Success';
                print(request.user)

    return JsonResponse(context)

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
            user = form.save()
            auth_login(request, user);
            return HttpResponseRedirect(reverse('homepage'))
        else:
            print(form.errors)
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
    listing = Listing.objects.raw("SELECT * FROM Listing WHERE Textbook_id = %s", [textbook_id])[0];
    return render(request, 'Product_Page.html', context={'listing': listing})

@login_required
def view_profile(request, account_username):
    account = Account.objects.raw("SELECT * FROM Account WHERE username = %s", [account_username])[0];
    return render(request, 'Other_Users_Profile.html', context={'account':account})

@login_required
def add_listing(request):
    form = forms.TextbookCreationForm();
    return render (request, "Add-Listing.html", context={'form':form})

@require_POST
@csrf_exempt
def add_listing_request(request):
    if request.is_ajax() == True:
        ISBN = request.POST.get('ISBN')
        Title = request.POST.get('Title')
        Author = request.POST.get('Author')
        Publisher = request.POST.get('Author')
        Condition = request.POST.get('Condition')
        Date_Published = request.POST.get('Date')
        Description = request.POST.get('Description')
        Image = request.FILES.get('Image')
        form = forms.TextbookCreationForm(request.POST);
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        """
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Textbook(ISBN, Title, Author, Publisher, Condition, Date_Published, Description, Image) VALUES(%s, %s, %s, %s, %s, %s, %s, Image)", [ISBN, Title, Author, Publisher, Condition, Date_Published, Description]);
            print("Inserted into database")
        """
    return JsonResponse({ 'message': 'Success', 'redirect': reverse('homepage')})
