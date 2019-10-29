from django.contrib import admin
from .models import Account, Textbook, Listing, Category, PaymentInfo, Order, Wishlist, Checkout
from .models import Category_Has_Textbook, Account_Has_PaymentInfo, Order_Contain_Textbook, Shopping_Cart


admin.site.register(Account)
admin.site.register(Textbook)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(PaymentInfo)
admin.site.register(Order)
admin.site.register(Wishlist)
admin.site.register(Checkout)
admin.site.register(Category_Has_Textbook)
admin.site.register(Account_Has_PaymentInfo)
admin.site.register(Order_Contain_Textbook)
admin.site.register(Shopping_Cart)
