import os, django, random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from faker import Faker
from main.models import Account

def create_account(N):
    fake = Faker()
    for i in range(N):
        first_name = fake.first_name()
        last_name = fake.last_name()
        Email = fake.email()
        Username = fake.user_name()
        Password = fake.password()
        Account.objects.get_or_create(first_name=first_name, last_name=last_name,email=Email,username=Username,password=Password)


create_account(30);
