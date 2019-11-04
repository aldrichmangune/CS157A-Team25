from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):

    Profile_Picture = models.ImageField(blank=True, null=True)

    class Meta:
        db_table = "Account"
        unique_together = ('username', 'email')

class Textbook(models.Model):

    Book_Condition_Choices = [
        ('MINT', 'BRAND NEW'),
        ('LIKE_NEW', 'LIKE NEW'),
        ('DECENT', 'GOOD'),
        ('FAIR', 'FAIR'),
        ('POOR', 'POOR'),
    ]

    ID = models.AutoField(primary_key=True)
    ISBN = models.BigIntegerField(blank=False)
    Title = models.CharField(max_length=100,blank=False)
    Image = models.ImageField(blank=True)
    Author = models.CharField(max_length=100,blank=False)
    Publisher = models.CharField(max_length=50,blank=False)
    Date_Published = models.DateField(blank=False)
    Condition = models.CharField(max_length=10, choices = Book_Condition_Choices, default='MINT')
    Description = models.CharField(max_length=5000,blank=False)

    def __str__(self):
        return "ID " + str(self.ID) + "-" + self.Title;

    class Meta:
        db_table = 'Textbook'
        unique_together=('ID', 'ISBN')

class Listing(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    Price = models.FloatField()
    def __str__(self):
        return self.Account.username + " listed " + self.Textbook.Title + " ID: " + str(self.Textbook.ID)\
            + " at $" + str(self.Price);

    class Meta:
        db_table = 'Listing'
        unique_together = ('Account', 'Textbook')

class Category(models.Model):
    Category_Name = models.CharField(primary_key= True, max_length=50)
    Description = models.CharField(max_length=1000);

    class Meta:
        db_table = 'Category'

class PaymentInfo(models.Model):
    Card_Number = models.BigIntegerField(primary_key=True)
    Card_Name = models.CharField(max_length=50)
    Security_Code = models.IntegerField()
    Card_Type = models.CharField(max_length=50)
    Zip_code = models.IntegerField()
    Expiration_Date = models.CharField(max_length=15)
    Billing_Address = models.CharField(max_length=100)

    class Meta:
        db_table = 'PaymentInfo'

class Order(models.Model):
    Order_ID = models.AutoField(primary_key=True)
    Date = models.DateTimeField()
    Shipping_Address = models.CharField(max_length=100)

    class Meta:
        db_table = 'Order'


class Wishlist(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Wishlist'
        unique_together = ('Account', 'Textbook')

class Checkout(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)


    class Meta:
        db_table = 'Checkout'
        unique_together = ('Account','Order')

class Category_Has_Textbook(models.Model):
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Category_Has_Textbook'
        unique_together = ('Category','Textbook')

class Account_Has_PaymentInfo(models.Model):
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    PaymentInfo = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Account_Has_PaymentInfo'
        unique_together = ('Account','PaymentInfo')

class Order_Contain_Textbook(models.Model):
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Order_Contain_Textbook'
        unique_together = ('Textbook','Order')

class Shopping_Cart(models.Model):
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Shopping_Cart'
        unique_together = ('Textbook', 'Account')
