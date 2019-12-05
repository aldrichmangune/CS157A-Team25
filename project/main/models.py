from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):

    """
    Account Table, inherits fields from AbstractUser along with a custom field Profile_Picture

    """
    Profile_Picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.username
    class Meta:
        db_table = "Account"
        # In every table row, username and email is unique together
        unique_together = ('username', 'email')

class Textbook(models.Model):

    """
    Textbook Table

    """

    # Choices for selecting condition of book
    Book_Condition_Choices = [
        ('MINT', 'BRAND NEW'),
        ('LIKE NEW', 'LIKE NEW'),
        ('DECENT', 'GOOD'),
        ('FAIR', 'FAIR'),
        ('POOR', 'POOR'),
    ]

    Textbook_ID = models.AutoField(primary_key=True)
    ISBN = models.BigIntegerField(blank=False)
    Title = models.CharField(max_length=100,blank=False)
    Image = models.ImageField(blank=True, null=True)
    Author = models.CharField(max_length=100,blank=False)
    Publisher = models.CharField(max_length=50,blank=False)

    Date_Published = models.DateField(blank=False)
    # Condition of Textbook field
    Cond = models.CharField(max_length=10, choices = Book_Condition_Choices, default='MINT')
    Description = models.CharField(max_length=5000,blank=False)

    def __str__(self):
        return "ID " + str(self.Textbook_ID) + "-" + self.Title;

    class Meta:
        db_table = 'Textbook'

        # Textbook_ID and ISBN together must be unique in every row of Textbook table
        unique_together=('Textbook_ID', 'ISBN')

class Listing(models.Model):
    """
    Table for relationship Listing

    """
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, db_column = 'Textbook_ID')
    Available = models.BooleanField(default=True)
    Price = models.FloatField()
    def __str__(self):
        return self.Account.username + " listed " + self.Textbook.Title + " ID: " + str(self.Textbook.Textbook_ID)\
            + " at $" + str(self.Price);

    class Meta:
        db_table = 'Listing'
        # Foreign Key Account and Textbook must be unique together in every row of table Listing
        unique_together = ('Account', 'Textbook')

class Category(models.Model):
    """
    Category Table

    """
    Category_Name = models.CharField(primary_key= True, max_length=50)

    def __str__(self):
        return self.Category_Name;

    class Meta:
        db_table = 'Category'

class PaymentInfo(models.Model):
    """
    PaymentInfo Table
    """

    Card_Number = models.BigIntegerField(primary_key=True)
    Card_Name = models.CharField(max_length=50)
    Security_Code = models.IntegerField()
    Expiration_Date = models.CharField(max_length=15)
    Billing_Address = models.CharField(max_length=100)

    def __str__(self):
        return self.Card_Name + " " + str(self.Card_Number)
    class Meta:
        db_table = 'PaymentInfo'

class Orders(models.Model):
    """
    Order Table
    """
    Order_ID = models.AutoField(primary_key=True)
    Date = models.DateTimeField()
    Shipping_Address = models.CharField(max_length=100)
    Shipping_Method = models.CharField(max_length=100)
    Total_Price = models.IntegerField()

    def __str__(self):
        return str(self.Order_ID) + " " + str(self.Total_Price) + " " + str(self.Date)

    class Meta:
        db_table = 'Orders'


class Wishlist(models.Model):
    """
    Table for relationship Wishlist

    """
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, db_column='Textbook_ID')

    def __str__(self):
        return self.Account.username + " " + self.Textbook.Title
    class Meta:
        db_table = 'Wishlist'
        # Foreign key Account and Textbook must be unique together in every row
        unique_together = ('Account', 'Textbook')

class Checkout(models.Model):
    """
    Table for relationship Checkout

    """
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    Order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='Order_ID')

    def __str__(self):
        return self.Account.username + " " + str(self.Order.Order_ID)

    class Meta:
        db_table = 'Checkout'
        # Foreign key Account and Order must be unique together in every row
        unique_together = ('Account','Order')

class Category_Has_Textbook(models.Model):
    """
    Table for relationship Category containing Textbooks

    """
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='Category_Name')
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, db_column='Textbook_ID')

    def __str__(self):
        return self.Category.Category_Name + ": " + self.Textbook.Title

    class Meta:
        db_table = 'Category_Has_Textbook'
        # Foreign key Category and Textbook must be unique together in every row
        unique_together = ('Category','Textbook')

class Account_Has_PaymentInfo(models.Model):
    """
    Table for relationship Account containing PaymentInfo

    """
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    PaymentInfo = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE, db_column='Card_Number')

    def __str__(self):
        return self.Account.username + " " + str(self.PaymentInfo.Card_Number)
    class Meta:
        db_table = 'Account_Has_PaymentInfo'
        # Foreign key Account and PaymentInfo must be unique together in every row
        unique_together = ('Account','PaymentInfo')

class Order_Contain_Textbook(models.Model):
    """
    Table for relationship Order containing Textbook

    """
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, db_column='Textbook_ID')
    Order = models.ForeignKey(Orders, on_delete=models.CASCADE, db_column='Order_ID')

    def __str__(self):
        return str(self.Order.Order_ID) + " " + self.Textbook.Title
    class Meta:
        db_table = 'Order_Contain_Textbook'
        # Foreign key Textbook and Order must be unique together in every row
        unique_together = ('Textbook','Order')

class Shopping_Cart(models.Model):
    """
    Table for relationship Shopping_Cart

    """
    Textbook = models.ForeignKey(Textbook, on_delete=models.CASCADE, db_column='Textbook_ID')
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.Account.username + " " + self.Textbook.Title
    class Meta:
        db_table = 'Shopping_Cart'
        # Foreign key Textbook and Account must be unique together in every row
        unique_together = ('Textbook', 'Account')
