from django.shortcuts import render
from django.http import HttpResponse
from db.models import Textbook

def index(request):
    t = Textbook.objects.all()
    html = "<html><body>The database currently contains these records: <br>"
    for text in t:
        html = html + text.textbook_text + "<br>"
    html = html + "</body></html>"
    return HttpResponse(html)
