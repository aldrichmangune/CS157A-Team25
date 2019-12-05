from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.core import serializers
from datetime import datetime
import json
import base64
from PIL import Image
from io import StringIO
from . import forms
from .models import Account, Textbook, Listing, Category_Has_Textbook, Category, Shopping_Cart, Wishlist
from .models import PaymentInfo, Orders, Checkout, Account_Has_PaymentInfo, Order_Contain_Textbook


def home(request):
    return HttpResponseRedirect(reverse('login'))

@login_required
def homepage(request):
    """
    Retrieve the logged in user's textbook listings and the amount of items in the user's shopping cart

    """

    listing_query = """
    SELECT *
    FROM Listing A, Textbook B
    WHERE A.Available = 1 AND A.Textbook_ID = B.Textbook_ID AND A.Account_id = %s
    """
    listings = Listing.objects.raw(listing_query, [str(request.user.id)])

    return render(request, 'Homepage.html',context={'listings':listings})

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
            context['password'] = 'Incorrect'
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
        password = make_password(request.POST.get('password1'))
        get_user_query = "SELECT * FROM Account WHERE username = %s"
        get_user_arguments = [request.POST.get('username')]
        user = Account.objects.raw(get_user_query, get_user_arguments)[:]
        if len(user) == 0:
            date_joined = datetime.now()
            password = make_password(request.POST.get('password1'))
            add_user_query = """INSERT INTO Account (username, password, email, first_name, last_name, date_joined,
                            is_staff, is_superuser, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            add_user_arguments = [request.POST.get('username'), password, request.POST.get('email'), request.POST.get('first_name'), request.POST.get('last_name'), date_joined, '1', '1', '1']
            with connection.cursor() as cursor:
                cursor.execute(add_user_query, add_user_arguments)
            connection.close()
            get_user_query = "SELECT * FROM Account WHERE username = %s AND password = %s"
            get_user_arguments.append(password)
            user = Account.objects.raw(get_user_query, get_user_arguments)[0]
            auth_login(request, user);
            request.user.is_superuser = False
            request.user.is_staff = False

            return HttpResponseRedirect(reverse('homepage'))
        else:
            pass

    return render(request, 'Register.html',context={'form':form});


@login_required
def my_profile(request):
    query = """
    SELECT *
    FROM Listing A, Textbook B
    WHERE A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
    AND A.Available = 1
    """
    my_listings = Listing.objects.raw(query, [str(request.user.id)])
    return render(request, 'Profile.html', context={'Listings': my_listings});

@login_required
def view_my_listings(request):
    active_listing_query = """
    SELECT *
    FROM Listing A, Textbook B
    WHERE A.Available = 1 AND A.Textbook_ID = B.Textbook_ID AND A.Account_id = %s
    """
    active_listings = Listing.objects.raw(active_listing_query, [str(request.user.id)])
    sold_listing_query = """
    SELECT A.id, E.username AS Buyer, Title, ISBN, Author, Publisher, Cond, Price
    FROM Listing A, Textbook B, Order_Contain_Textbook C, Checkout D, Account E
    WHERE A.Account_id = %s AND A.Textbook_ID = B.Textbook_ID
    AND C.Textbook_ID = B.Textbook_ID AND D.Order_ID = C.Order_ID
    AND E.ID = D.Account_ID AND Available = 0
    """

    Sold_Listings = Listing.objects.raw(sold_listing_query, [str(request.user.id)])
    Sold_Listings = Sold_Listings[:]

    return render(request, 'My_Listings.html', context={'active_listings': active_listings, 'sold_listings': Sold_Listings});
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
                password = make_password(request.POST.get('password'))
                if request.user.check_password(request.POST.get('password')):
                    pass;
                else:
                    cursor.execute("UPDATE Account SET password = %s WHERE username = %s;", [password, request.user.username])
                    user = Account.objects.raw('SELECT * FROM Account WHERE username = %s AND password = %s', [request.user.username, password])[0]
                    auth_login(request, user);

                if request.FILES.get('Profile_Picture') is not None:
                    request.user.Profile_Picture = request.FILES.get('Profile_Picture');
                    request.user.save()

                cursor.execute("UPDATE Account SET email = %s, first_name = %s, last_name = %s WHERE username = %s;", [request.POST.get('email'), request.POST.get('first_name'), request.POST.get('last_name'), request.user.username])

                modified_data['email'] = request.POST.get('email')
                modified_data['first_name'] = request.POST.get('first_name')
                modified_data['last_name'] = request.POST.get('last_name')
                new_form = forms.AccountChangeForm(initial=modified_data)
                auth_login(request, request.user)
                return render(request, 'Settings.html', context={'form': new_form})
            else:
                print(form.errors)

        connection.close()
    return render(request, 'Settings.html',context={'form':form});


@login_required
def view_product_page(request, textbook_id):
    query = """
    SELECT *
    FROM Listing A, Textbook B, Account C
    WHERE A.Available = 1 AND A.Account_id = C.id AND A.Textbook_ID = B.Textbook_ID AND A.Textbook_ID = %s
    """
    listing = Listing.objects.raw(query, [textbook_id])[0];

    Cart = Shopping_Cart.objects.raw("SELECT * FROM Shopping_Cart WHERE Account_ID = %s AND Textbook_ID = %s", [str(request.user.id), textbook_id])
    Wish_list = Wishlist.objects.raw("SELECT * FROM Wishlist WHERE Account_ID = %s AND Textbook_ID = %s", [str(request.user.id), textbook_id])
    Cart = Cart[:]
    Wish_list = Wish_list[:]
    Listing_In_Cart = False
    Listing_In_Wishlist = False
    if len(Cart) == 1:
        Listing_In_Cart = True
    if len(Wish_list) == 1:
        Listing_In_Wishlist = True
    # If the listing is listed by the user, then return a view that lets the user edit the listing information instead
    if listing.username == request.user.username:
        Category_Query = """
        SELECT id, A.Category_Name
        FROM Category_Has_Textbook A, Category B
        WHERE B.Category_Name = A.Category_Name AND A.Textbook_ID = %s
        """
        Categories = Category.objects.raw(Category_Query, [textbook_id])

        data = {'ISBN': listing.ISBN,'Title': listing.Title,'Author': listing.Author,'Publisher': listing.Publisher,'Cond': listing.Cond,
                'Date_Published': listing.Date_Published, 'Price': listing.Price, 'Description': listing.Description,'Image': listing.Image
                ,'Category': Categories}
        form = forms.TextbookChangeForm(initial=data)
        return render(request, 'My_Product_Page.html', context={'form': form, 'listing': listing})

    return render(request, 'Product_Page.html', context={'listing': listing, 'Cart': Listing_In_Cart, 'Wishlist': Listing_In_Wishlist})

@login_required
def view_profile(request, account_username):
    account = Account.objects.raw("SELECT * FROM Account WHERE username = %s", [account_username])[0];
    listing_query = """
    SELECT *
    FROM Listing A, Textbook B, Account C
    WHERE C.username = %s AND A.Account_id = C.id AND B.Textbook_ID = A.Textbook_ID
    AND A.Available = 1
    """
    listings = Listing.objects.raw(listing_query, [account_username])
    return render(request, 'Other_Users_Profile.html', context={'account':account, 'Listings': listings})

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
            insert_textbook_query = """
            INSERT INTO
            Textbook (ISBN, Title, Author, Publisher, Date_Published, Description, Cond)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_textbook_query,(ISBN, Title, Author, Publisher, Date_Published, Description, Cond));
            Textbook_id = cursor.lastrowid
            # For each category that the textbook belongs to, create a corresponding Category_Has_Textbook row
            for C in Categories:
                temp = Category.objects.raw("Select * From Category Where Category_Name = %s", [C])[0]
                cursor.execute("INSERT INTO Category_Has_Textbook (Category_Name, Textbook_ID) VALUES (%s, %s)", [temp.Category_Name, Textbook_id])
            cursor.execute("INSERT INTO Listing (Price, Account_id, Textbook_ID, Available) VALUES (%s, %s, %s, %s)", (Price, request.user.id, Textbook_id, '1'))
        connection.close()

        book = Textbook.objects.raw("Select * From Textbook WHERE Textbook_ID= %s", [Textbook_id])[0]
        book.Image = Image;
        book.save();
    else:
        print(form.errors);
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def my_listings(request):
    listings = Listing.objects.raw("Select * From Listing WHERE Available = 1 AND Account_id = %s", [request.user.id])
    return render(request, "my-listing.html", context={'listings':listings});

@login_required
def view_shopping_cart(request):
    shopping_cart_query = """
            SELECT *
            FROM Shopping_Cart A, Listing B, Textbook C
            WHERE B.Available = 1 AND A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
            AND A.Textbook_ID = C.Textbook_ID
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

        shopping_cart_query = """
        SELECT *
        FROM Shopping_Cart A, Listing B, Textbook C
        WHERE B.Available = 1 AND A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
        AND A.Textbook_ID = C.Textbook_ID
        """

        Cart = Shopping_Cart.objects.raw(shopping_cart_query, [str(request.user.id)])
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
        cart_query = "SELECT * FROM Shopping_Cart WHERE Textbook_ID = %s"
        cart = Shopping_Cart.objects.raw(cart_query, [textbook_id])[:]
        if len(cart) == 0:
            with connection.cursor() as cursor:
                # Insert the item into the user's shopping cart
                cursor.execute("INSERT INTO Shopping_Cart(Textbook_ID, Account_ID) VALUES(%s, %s)", [textbook_id, str(request.user.id)])
            connection.close()
        return JsonResponse({})

@login_required
def view_wishlist(request):
    wishlist_query = """
            SELECT *
            FROM Wishlist A, Listing B, Textbook C
            WHERE B.Available = 1 AND A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
            AND A.Textbook_ID = C.Textbook_ID
            """
    Wish_list= Wishlist.objects.raw(wishlist_query, [str(request.user.id)])
    return render(request, "Wishlist.html",context={'Wishlist': Wish_list})

@login_required
@csrf_exempt
@require_POST
def add_to_wishlist(request):
    if request.is_ajax() == True:
        context = {}
        textbook_id = request.POST.get('textbook_id')
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Wishlist(Textbook_ID, Account_ID) VALUES(%s, %s)", [textbook_id, str(request.user.id)])
        connection.close()
        Wish_list = Wishlist.objects.raw("SELECT * FROM Wishlist WHERE Account_ID = %s", [str(request.user.id)])
        Wish_list = Wish_list[:]
        context={'wishlist_length': len(Wish_list)}
        return JsonResponse(context)

@login_required
@csrf_exempt
@require_POST
def remove_from_wishlist(request):
    if request.is_ajax() == True:
        textbook_id = request.POST.get('textbook_id')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM Wishlist WHERE Account_ID = %s and Textbook_ID = %s", [str(request.user.id), textbook_id])
        connection.close()

        wish_list_query = """
        SELECT *
        FROM Wishlist A, Listing B, Textbook C
        WHERE B.Available = 1 AND A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
        AND A.Textbook_ID = C.Textbook_ID
        """
        Wish_list = Wishlist.objects.raw(wish_list_query, [str(request.user.id)])
        refresh = request.POST.get('refresh')
        if refresh == 'False':
            return JsonResponse({})
        else:
            return render(request, "Wishlist_Items.html",context={'Wishlist': Wish_list})

@login_required
@csrf_exempt
def check_payment_info(request):
    if request.is_ajax() == True:
        Billing_Address = request.GET.get('billing_address')
        Credit_Card_Number = request.GET.get('credit_card_number')
        Credit_Card_Name = request.GET.get('credit_card_name')
        Credit_Card_Security_Code = request.GET.get('credit_card_cvv')
        Credit_Card_Expire_Date = request.GET.get('credit_card_expiration')
        query = "SELECT * FROM PaymentInfo WHERE Card_Number = %s"
        result = PaymentInfo.objects.raw(query, [Credit_Card_Number])[:]
        if(len(result) == 0):
            return JsonResponse({'message': 'Valid'})
        else:
            result = result[0]
            if result.Card_Name != Credit_Card_Name or str(result.Security_Code) != Credit_Card_Security_Code or result.Expiration_Date != Credit_Card_Expire_Date or result.Billing_Address != Billing_Address:
                return JsonResponse({'message': 'Invalid'})
            else:
                return JsonResponse({'message': 'Valid'})


@login_required
def view_checkout(request):
    shopping_cart_query = """
            SELECT *
            FROM Shopping_Cart A, Listing B, Textbook C
            WHERE B.Available = 1 AND A.Account_ID = %s AND A.Textbook_ID = B.Textbook_ID
            AND A.Textbook_ID = C.Textbook_ID
            """
    credit_card_query = """
    SELECT *
    FROM PaymentInfo A, Account_Has_PaymentInfo B
    WHERE A.Card_Number = B.Card_Number AND B.Account_ID = %s
    """
    Credit_Cards = PaymentInfo.objects.raw(credit_card_query, [str(request.user.id)])
    Cart = Shopping_Cart.objects.raw(shopping_cart_query, [str(request.user.id)])
    return render(request, 'Checkout.html', context={"Cart": Cart, 'Credit_Cards': Credit_Cards})

@login_required
def view_credit_cards(request):
    Credit_Cards = PaymentInfo.objects.raw("SELECT * FROM PaymentInfo A, Account_Has_PaymentInfo B WHERE A.Card_Number = B.Card_Number AND B.Account_ID = %s", [str(request.user.id)])
    return render(request, 'My_Credit_Cards.html', context={'Credit_Cards': Credit_Cards})

@login_required
@require_POST
@csrf_exempt
def checkout_request(request):
    if request.is_ajax() == True:
        Textbooks = json.loads(request.POST.get('textbooks'))
        Shipping_Address = request.POST.get('shipping_address')
        Shipping_Method = request.POST.get('Shipping_Method')
        Billing_Address = request.POST.get('billing_address')
        Total_Price = request.POST.get('order_total_price')
        Credit_Card_Number = request.POST.get('credit_card_number')
        Credit_Card_Name = request.POST.get('credit_card_name')
        Credit_Card_Security_Code = request.POST.get('credit_card_cvv')
        Credit_Card_Expire_Date = request.POST.get('credit_card_expiration')
        Present_Time = datetime.now()
        with connection.cursor() as cursor:
            payment_info_query = "SELECT * FROM PaymentInfo WHERE Card_Number = %s"
            Credit_Card = PaymentInfo.objects.raw(payment_info_query, [Credit_Card_Number])[:]
            if len(Credit_Card) == 0:
                insert_payment_info_query = """
                INSERT INTO PaymentInfo(Card_Number, Card_Name, Security_Code, Expiration_Date, Billing_Address)
                VALUES(%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_payment_info_query, [Credit_Card_Number, Credit_Card_Name, Credit_Card_Security_Code, Credit_Card_Expire_Date, Billing_Address])

            account_has_payment_info_query = """
            SELECT * FROM Account_Has_PaymentInfo
            WHERE Account_id = %s AND Card_Number = %s
            """
            result = Account_Has_PaymentInfo.objects.raw(account_has_payment_info_query, [str(request.user.id), Credit_Card_Number])[:]
            if len(result) == 0:
                insert_account_has_payment_info_query = """
                INSERT INTO Account_Has_PaymentInfo(Account_id, Card_Number)
                VALUES (%s, %s)
                """
                cursor.execute(insert_account_has_payment_info_query, [str(request.user.id), Credit_Card_Number])

            insert_order_query = """
            INSERT INTO Orders(Date, Shipping_Address, Shipping_Method, Total_Price)
            VALUES(%s, %s, %s, %s)
            """
            cursor.execute(insert_order_query, [Present_Time, Shipping_Address, Shipping_Method, Total_Price])
            Order_ID = cursor.lastrowid

            insert_checkout_query = "INSERT INTO Checkout(Account_id, Order_ID) VALUES(%s, %s)"
            cursor.execute(insert_checkout_query, [str(request.user.id), Order_ID])

            for item in Textbooks:
                delete_from_shopping_carts_query = "DELETE FROM Shopping_Cart WHERE Textbook_ID = %s"
                delete_from_wishlists_query = "DELETE FROM Wishlist WHERE Textbook_ID = %s"
                update_listing_query = "UPDATE Listing SET Available = 0 WHERE Textbook_ID = %s"
                insert_order_contains_textbook_query = """
                INSERT INTO Order_Contain_Textbook(Textbook_ID, Order_ID)
                VALUES(%s, %s)
                """
                cursor.execute(delete_from_shopping_carts_query, [item])
                cursor.execute(delete_from_wishlists_query, [item])
                cursor.execute(update_listing_query, [item])
                cursor.execute(insert_order_contains_textbook_query, [item, Order_ID])
        connection.close()
    return JsonResponse({'redirect': reverse('homepage')})

@login_required
def view_orders(request):
    Checkouts = Checkout.objects.raw("SELECT * FROM Checkout WHERE Account_id = %s ORDER BY Order_ID DESC;", [str(request.user.id)])
    Checkouts = Checkouts[:]
    Orders = {}
    for checkout in Checkouts:
        textbooks_query = """
        SELECT *
        FROM Checkout A, Orders B, Order_Contain_Textbook C, Textbook D, Listing E
        WHERE A.Account_id = %s AND A.Order_ID = B.Order_ID AND A.Order_ID = C.Order_ID
        AND D.Textbook_ID = C.Textbook_ID AND E.Textbook_ID = D.Textbook_ID
        AND E.Available = 0 AND A.Order_ID = %s
        """
        list_of_textbooks = Order_Contain_Textbook.objects.raw(textbooks_query, [str(request.user.id), str(checkout.Order.Order_ID)])
        list_of_textbooks = list_of_textbooks[:]
        sellers_query = """
        SELECT *
        FROM Account A, Listing B, Order_Contain_Textbook C
        WHERE A.id = B.Account_ID AND B.Available = 0 AND B.Textbook_ID = C.Textbook_ID AND C.Order_ID = %s
        """
        list_of_sellers = Account.objects.raw(sellers_query, [str(checkout.Order.Order_ID)])
        list_of_sellers = list_of_sellers[:]
        Orders[checkout.Order.Order_ID] = zip(list_of_textbooks, list_of_sellers)
    return render(request, 'Orders.html', context={'Orders': Orders})

@login_required
def search(request):

    # Query all the Categories and textbook Listings in the database
    Categories = Category.objects.raw("Select * FROM Category")
    search_query = """
    Select *
    FROM Listing A, Textbook B
    WHERE A.Textbook_ID = B.Textbook_ID AND A.Available = 1
    AND A.Account_ID <> """ + str(request.user.id) + """ ORDER BY Title DESC;
    """
    Listings = Listing.objects.raw(search_query)

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
                results = Listing.objects.raw("SELECT * FROM Listing A, Textbook B WHERE A.Available = 1 AND A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " "  + sort + ";")
            else:

                results = Listing.objects.raw("SELECT * FROM Listing A, Textbook B WHERE A.Available = 1 AND A.Textbook_ID = B.Textbook_ID AND A.Account_ID <> " + str(request.user.id) + " AND " + filter + " LIKE '%" + text + "%' " + sort + ";")

        else:
            # If a Category is selected, do the same as above but this time adds condition to ensure that
            # the textbook belongs to at least 1 of the category selected
            query = """
            SELECT DISTINCT A.Textbook_ID, A.id, Title, Author, ISBN, Price, Cond
            FROM Listing A, Textbook B, Category_Has_Textbook C
            WHERE A.Available = 1 AND A.Textbook_ID = B.Textbook_ID
            AND A.Account_ID <> """ + str(request.user.id) + """ AND B.Textbook_ID = C.Textbook_ID
            AND C.Category_Name IN (
            """
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
