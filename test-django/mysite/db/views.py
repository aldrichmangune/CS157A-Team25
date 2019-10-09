from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.template.response import TemplateResponse
from django.utils import timezone

from db.models import Textbook


def index(request):
    t = Textbook.objects.all()
    html = "<html><body>The database currently contains these records: <br>"
    for text in t:
        html = html + text.textbook_text + "<br>"
    html = html + "</body></html>"
    return HttpResponse(html)

def createTextbook(request):
    if request.method == 'POST':
        if request.POST.get('title'):
            Textbook(textbook_text=request.POST.get('title'), pub_date=timezone.now()).save()
            return HttpResponse("Successfully posted " + request.POST.get('title'))
        else:
            return HttpResponse("Something went wrong")
    else:
        return TemplateResponse(request, 'db/create_listing.html')