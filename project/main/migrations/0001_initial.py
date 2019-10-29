# Generated by Django 2.2.6 on 2019-10-29 04:56

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('Profile_Picture', models.ImageField(blank=True, null=True, upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Account',
                'unique_together': {('username', 'email')},
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('Category_Name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('Description', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'Category',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('Order_ID', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateTimeField()),
                ('Shipping_Address', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.CreateModel(
            name='PaymentInfo',
            fields=[
                ('Card_Number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('Card_Name', models.CharField(max_length=50)),
                ('Security_Code', models.IntegerField()),
                ('Card_Type', models.CharField(max_length=50)),
                ('Zip_code', models.IntegerField()),
                ('Expiration_Date', models.CharField(max_length=15)),
                ('Billing_Address', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'PaymentInfo',
            },
        ),
        migrations.CreateModel(
            name='Textbook',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('ISBN', models.BigIntegerField()),
                ('Title', models.CharField(max_length=100)),
                ('Image', models.ImageField(blank=True, upload_to='')),
                ('Author', models.CharField(max_length=100)),
                ('Publisher', models.CharField(max_length=50)),
                ('Year_Of_Publication', models.DateField()),
                ('Description', models.CharField(max_length=5000)),
            ],
            options={
                'db_table': 'Textbook',
                'unique_together': {('ID', 'ISBN')},
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Textbook')),
            ],
            options={
                'db_table': 'Wishlist',
                'unique_together': {('Account', 'Textbook')},
            },
        ),
        migrations.CreateModel(
            name='Shopping_Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Textbook')),
            ],
            options={
                'db_table': 'Shopping_Cart',
                'unique_together': {('Textbook', 'Account')},
            },
        ),
        migrations.CreateModel(
            name='Order_Contain_Textbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
                ('Textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Textbook')),
            ],
            options={
                'db_table': 'Order_Contain_Textbook',
                'unique_together': {('Textbook', 'Order')},
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Price', models.FloatField()),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Textbook')),
            ],
            options={
                'db_table': 'Listing',
                'unique_together': {('Account', 'Textbook')},
            },
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Order')),
            ],
            options={
                'db_table': 'Checkout',
                'unique_together': {('Account', 'Order')},
            },
        ),
        migrations.CreateModel(
            name='Category_Has_Textbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Category')),
                ('Textbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Textbook')),
            ],
            options={
                'db_table': 'Category_Has_Textbook',
                'unique_together': {('Category', 'Textbook')},
            },
        ),
        migrations.CreateModel(
            name='Account_Has_PaymentInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('PaymentInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.PaymentInfo')),
            ],
            options={
                'db_table': 'Account_Has_PaymentInfo',
                'unique_together': {('Account', 'PaymentInfo')},
            },
        ),
    ]