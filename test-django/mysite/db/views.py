from django.shortcuts import render
from django.http import HttpResponse
from db.models import Textbook

def index(request):
    t = Textbook.objects.all()
    return HttpResponse("Hello, world. " + text.textbook_text for text in t)
