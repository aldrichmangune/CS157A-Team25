from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core import serializers
from datetime import datetime
import json
from . import forms
from .models import Account, Textbook, Listing, Category_Has_Textbook, Category, Shopping_Cart


def home(request):
    return HttpResponseRedirect(reverse('login'))

@login_required
def homepage(request):
    """
    Retrieve the logged in user's textbook listings and the amount of items in the user's shopping cart

    """

    listing_query = "Select * from Listing A, Textbook B WHERE A.Textbook_ID = B.Textbook_ID AND A.Account_id = %s"
    listings = Listing.objects.raw(listing_query, [str(request.user.id)]);

    cart_query = "SELECT * FROM Shopping_Cart WHERE Account_ID = %s"
    Cart = Shopping_Cart.objects.raw(cart_query, [str(request.user.id)])

    # Slice Cart to unwrap the RawQueryset into a list
    Cart = Cart[:]
    return render(request, 'Homepage.html',context={'listings':listings, 'cart_length': len(Cart)})

def login(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect(reverse('homepage'))
    return render(request, 'Login.html');

@require_POST
@csrf_exempt
def login_request(request):
    """
    Process the login request by querying the database for an existing Account given user input
    and returns a JsonResponse to the ajax call

    """

    context = {}
    if request.is_ajax() == True:
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
            add_user_query = "INSERT INTO Account (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s);"
            add_user_arguments = [request.POST.get('username'), request.POST.get('password1'), request.POST.get('email'), request.POST.get('first_name'), request.POST.get('last_name')]

            with connection.cursor() as cursor:
                cursor.execute(add_user_query, add_user_arguments)
            connection.close()

            get_user_query = "SELECT * FROM Account WHERE username = %s and password = %s"
            get_user_arguments = [request.POST.get('username'), request.POST.get('password1')]
            user = Account.objects.raw(get_user_query, get_user_arguments)[0]
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

    user_query = "SELECT * FROM Account WHERE username = %s;"
    user_query_arguments = [request.user.username]

    user = Account.objects.raw(user_query, user_query_arguments)[0]
    data = {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}

    # Populate the form with the user's email, first name, last name
    form = forms.AccountChangeForm(initial=data)

    if request.method == 'POST':
        form = forms.AccountChangeForm(request.POST)

        with connection.cursor() as cursor:
            if(form.is_valid()):
                modified_data = {};

                if request.user.check_password(request.POST.get('password')):
                    pass;
                else:
                    cursor.execute("UPDATE Account SET password = %s WHERE username = %s;", [request.POST.get('password'), request.user.username])
                    auth_login(request, user);

                if request.FILES.get('Profile_Picture') is not None:
                    request.user.Profile_Picture = request.FILES.get('Profile_Picture');
                    request.user.save()

                cursor.execute("UPDATE Account SET email = %s, first_name = %s, last_name = %s WHERE username = %s;", [request.POST.get('email'), request.POST.get('first_name'), request.POST.get('last_name'), request.user.username])

                modified_data['email'] = request.POST.get('email')
                modified_data['first_name'] = request.POST.get('first_name')
                modified_data['last_name'] = request.POST.get('last_name')
                new_form = forms.AccountChangeForm(initial=modified_data)

                return render(request, 'Settings.html', context={'form': new_form})
            else:
                print(form.errors)

        connection.close()
    return render(request, 'Settings.html',context={'form':form});


@login_required
def view_product_page(request, textbook_id):
    query = "SELECT * FROM Listing A, Textbook B, Account C WHERE A.Account_id = C.id AND A.Textbook_ID = B.Textbook_ID AND A.Textbook_ID = %s"
    listing = Listing.objects.raw(query, [textbook_id])[0];
    Cart = Shopping_Cart.objects.raw("SELECT * FROM Shopping_Cart WHERE Account_ID = %s", [str(request.user.id)])

    Listing_In_Cart = False
    for item in Cart:
        if listing.Textbook == item.Textbook:
            Listing_In_Cart = True

    # If the listing is listed by the user, then return a view that lets the user edit the listing information instead
    if listing.username == request.user.username:
        Categories = Category.objects.raw("SELECT id, A.Category_Name FROM Category_Has_Textbook A, Category B WHERE B.Category_Name = A.Category_Name AND A.Textbook_ID = %s", [textbook_id])
        data = {'ISBN': listing.ISBN,'Title': listing.Title,'Author': listing.Author,'Publisher': listing.Publisher,'Cond': listing.Cond,
                'Date_Published': listing.Date_Published, 'Price': listing.Price, 'Description': listing.Description,'Image': listing.Image
                ,'Category': Categories}
        form = forms.TextbookChangeForm(initial=data)
        return render(request, 'My_Product_Page.html', context={'form': form, 'listing': listing})

    return render(request, 'Product_Page.html', context={'listing': listing, 'Cart': Listing_In_Cart})

@login_required
def view_profile(request, account_username):
    account = Account.objects.raw("SELECT * FROM Account WHERE username = %s", [account_username])[0];
    return render(request, 'Other_Users_Profile.html', context={'account':account})

@login_required
def add_listing(request):
    data = {'Date_Published': datetime.now()}
    form = forms.TextbookCreationForm(initial=data);
    return render(request, "Add-Listing.html", context={'form':form})

@login_required
@require_POST
@csrf_exempt
def cancel_listing_request(request):
    context={}
    if request.is_ajax() == True:
        textbook_id = request.POST.get('textbook-id')
        with connection.cursor() as cursor:
            # DELETE all Category_Has_Textbook, Listing, Wishlist, Shopping_Cart rows that the textbook belongs to
            # and then delete the Textbook
            cursor.execute("DELETE FROM Category_Has_Textbook WHERE Textbook_ID = %s;", [textbook_id])
            cursor.execute("DELETE FROM Listing WHERE Textbook_ID = %s;", [textbook_id])
            cursor.execute("DELETE FROM Wishlist WHERE Textbook_ID = %s;", [textbook_id])
            cursor.execute("DELETE FROM Shopping_Cart WHERE Textbook_ID = %s;", [textbook_id])
            cursor.execute("DELETE FROM Textbook WHERE Textbook_ID = %s;", [textbook_id])
        connection.close()
        context['message'] = 'Success'
        context['redirect'] = reverse('homepage')
    else:
        context['message'] = 'Fail'
    return JsonResponse(context)

@login_required
@require_POST
def edit_listing_request(request):

    form = forms.TextbookChangeForm(request.POST)
    if form.is_valid():

        Book = Textbook.objects.raw("SELECT * FROM Textbook WHERE Textbook_ID = %s", [request.POST.get('textbook_id')])[0]
        List = Listing.objects.raw("SELECT * FROM Listing WHERE Textbook_ID = %s", [request.POST.get('textbook_id')])[0]
        Date_Published = request.POST.get('Date_Published_year') + "-" + request.POST.get('Date_Published_month') + "-" + request.POST.get('Date_Published_day');
        Categories = Category_Has_Textbook.objects.raw("SELECT * FROM Category_Has_Textbook WHERE Textbook_ID = %s", [request.POST.get('textbook_id')])
        Category_List = request.POST.getlist('Category')

        with connection.cursor() as cursor:
            # If the textbook no longer belong to that Category, DELETE the corresponding Category_Has_Textbook row
            for C in Categories:
                if C.Category not in Category_List:
                    cursor.execute("DELETE FROM Category_Has_Textbook WHERE Category_Name = %s AND Textbook_ID = %s", [C.Category.Category_Name, request.POST.get('textbook_id')])

            # Select the remaining Category that the Textbook belongs to
            Categories = Category_Has_Textbook.objects.raw("SELECT * FROM Category_Has_Textbook WHERE Textbook_ID = %s", [request.POST.get('textbook_id')])

            # Slices it to unwrap the RawQueryset into a list
            temp = Categories[:]
            Categories = []

            # Append the name of each category that the textbook belongs to into a list
            for t in temp:
                Categories.append(t.Category)

            # If a category that the textbook belongs to already has a Category_Has_Textbook row, ignores it
            # otherwises create a new Category_Has_Textbook row
            for C in Category_List:
                if C in Categories:
                    pass
                else:
                    cursor.execute("INSERT INTO Category_Has_Textbook (Category_Name, Textbook_ID) VALUES (%s, %s)", [C, request.POST.get('textbook_id')])

            # Update the information about the textbook as well as the price for the listings

            update_textbook_query = """UPDATE Textbook SET ISBN = %s, Title = %s, Author = %s, Publisher = %s,
            Cond = %s, Description = %s, Date_Published = %s WHERE Textbook_ID = %s;"""
            update_textbook_arguments = [request.POST.get('ISBN'), request.POST.get('Title'), request.POST.get('Author'), request.POST.get('Publisher'), request.POST.get('Cond'), request.POST.get('Description'), Date_Published, request.POST.get('textbook_id')]
            cursor.execute(update_textbook_query, update_textbook_arguments)

            update_listing_query = "UPDATE Listing SET Price = %s WHERE Textbook_ID = %s;"
            update_listing_arguments = [request.POST.get('Price'), request.POST.get('textbook_id')]
            cursor.execute(update_listing_query, update_listing_arguments)

            if request.FILES.get('Image') != None:
                Book.Image = request.FILES.get('Image')
                Book.save()

        connection.close()

    return HttpResponseRedirect(reverse('homepage'))

@login_required
@require_POST
def add_listing_request(request):

    ISBN = request.POST.get('ISBN')
    Title = request.POST.get('Title')
    Author = request.POST.get('Author')
    Publisher = request.POST.get('Publisher')
    Cond = request.POST.get('Cond')
    Date_Published = request.POST.get('Date_Published_year') + "-" + request.POST.get('Date_Published_month') + "-" + request.POST.get('Date_Published_day');
    Price = request.POST.get('Price')
    Description = request.POST.get('Description')
    Image = request.FILES.get('Image')

    form = forms.TextbookCreationForm(request.POST);
    Categories = request.POST.getlist('Category')

    if form.is_valid():
        Textbook_id = None;

        # Insert a new Textbook into the database
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Textbook (ISBN, Title, Author, Publisher, Date_Published, Description, Cond) VALUES (%s, %s, %s, %s, %s, %s, %s)",(ISBN, Title, Author, Publisher, Date_Published, Description, Cond));
            Textbook_id = cursor.lastrowid

            # For each category that the textbook belongs to, create a corresponding Category_Has_Textbook row
            for C in Categories:
                temp = Category.objects.raw("Select * From Category Where Category_Name = %s", [C])[0]
                cursor.execute("Insert into Category_Has_Textbook (Category_Name, Textbook_ID) VALUES (%s, %s)", [temp.Category_Name, Textbook_id])
            cursor.execute("INSERT INTO Listing (Price, Account_id, Textbook_ID) VALUES (%s, %s, %s)", (Price, request.user.id, Textbook_id))
        connection.close()

        book = Textbook.objects.raw("Select * From Textbook WHERE Textbook_ID= %s", [Textbook_id])[0]
        book.Image = Image;
        book.save();
    else:
        print(form.errors);
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def my_listings(request):
    listings = Listing.objects.raw("Select * From Listing WHERE Account_id = %s", [request.user.id])
    return render(request, "my-listing.html", context={'listings':listings});

@login_required
def view_shopping_cart(request):
    shopping_cart_query = """
            SELECT *
            FROM Shopping_Cart A, Listing B, Textbook C
            WHERE A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID AND A.Textbook_ID = C.Textbook_ID
            """
    Cart = Shopping_Cart.objects.raw(shopping_cart_query, [str(request.user.id)])
    total_price = 0;
    for item in Cart:
        total_price += item.Price
    return render(request, "Shopping_Cart.html",context={'Cart': Cart, 'total_price': total_price})

@login_required
@csrf_exempt
@require_POST
def shopping_cart_delete(request):

    if request.is_ajax() == True:
        textbook_id = request.POST.get('textbook_id')
        with connection.cursor() as cursor:
            # Delete the item from the user's shopping cart
            cursor.execute("DELETE FROM Shopping_Cart WHERE Account_ID = %s and Textbook_ID = %s", [str(request.user.id), textbook_id])
        connection.close()

        Cart = Shopping_Cart.objects.raw("SELECT * FROM Shopping_Cart A, Listing B, Textbook C WHERE A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID AND A.Textbook_ID = C.Textbook_ID", [str(request.user.id)])
        total_price = 0;
        for item in Cart:
            total_price += item.Price
        return render(request, "Cart_Items.html",context={'Cart': Cart, 'total_price': total_price})

@login_required
@csrf_exempt
@require_POST
def add_to_cart(request):
    if request.is_ajax() == True:
        context = {}
        textbook_id = request.POST.get('textbook_id')
        with connection.cursor() as cursor:
            # Insert the item into the user's shopping cart
            cursor.execute("INSERT INTO Shopping_Cart(Textbook_ID, Account_ID) VALUES(%s, %s)", [textbook_id, str(request.user.id)])
        connection.close()
        Cart = Shopping_Cart.objects.raw("SELECT * FROM Shopping_Cart WHERE Account_ID = %s", [str(request.user.id)])
        Cart = Cart[:]
        context={'cart_length': len(Cart)}
        return JsonResponse(context)

@login_required
def checkout(request):
    return render(request, 'Checkout.html')


@login_required
def search(request):

    # Query all the Categories and textbook Listings in the database
    Categories = Category.objects.raw("Select * FROM Category")
    Listings = Listing.objects.raw("Select * FROM Listing A, Textbook B WHERE A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " ORDER BY Title DESC;")

    return render(request, 'search.html', context={'Categories': Categories, 'listings': Listings});

@login_required
@csrf_exempt
def search_request(request):

    results = None;
    if request.is_ajax() == True:
        Categories = json.loads(request.GET.get('Categories'))
        Sort_ID = request.GET.get('Sort')
        text = request.GET.get('search-text')
        filter = request.GET.get('select-filter')
        sort = sort_order(Sort_ID)

        if len(Categories) == 0:
            # If no Category option is selected and search-bar text is empty, then simply returns a
            # search query containing every textbook listing ordered by selected sorting order
            # Else, search for all textbook listings where the filter such as ISBN, Title, Author matches the pattern
            # in the search bar
            if text == '':
                results = Listing.objects.raw("SELECT * FROM Listing A, Textbook B WHERE A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " "  + sort + ";")
            else:

                results = Listing.objects.raw("SELECT * FROM Listing A, Textbook B WHERE A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " AND " + filter + " LIKE '%" + text + "%' " + sort + ";")

        else:
            # If a Category is selected, do the same as above but this time adds condition to ensure that
            # the textbook belongs to at least 1 of the category selected
            query = "SELECT DISTINCT A.Textbook_ID, A.id, Title, Author, ISBN, Price, Cond FROM Listing A, Textbook B, Category_Has_Textbook C WHERE A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " AND B.Textbook_ID = C.Textbook_ID AND C.Category_Name IN ("
            for category in Categories:
                query += "'" + Categories[category] + "', "
            if text == '':
                query = query[:-2] + ") " + sort + ";"
                results = Listing.objects.raw(query)
            else:
                query = query[:-2] + ") AND " + filter + " LIKE '%" + text + "%' " + sort + ";"
                results = Listing.objects.raw(query)
    return render(request, 'search_results.html', context={'listings': results})

def sort_order(Sort_ID):
    sort = None;
    if Sort_ID == '1':
        sort = "ORDER BY Title DESC"
    elif Sort_ID == '2':
        sort = "ORDER BY Title ASC"
    elif Sort_ID == '3':
        sort = "ORDER BY Author DESC"
    elif Sort_ID == '4':
        sort = "ORDER BY Author ASC"
    elif Sort_ID == '5':
        sort = "ORDER BY ISBN DESC"
    elif Sort_ID == '6':
        sort = "ORDER BY ISBN ASC"
    elif Sort_ID == '7':
        sort = "ORDER BY Price ASC"
    elif Sort_ID == '8':
        sort = "ORDER BY Price DESC"
    return sort
