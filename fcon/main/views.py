from unicodedata import name
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from main.models import Sheet
from .forms import sheetCreator

# Create your views here.

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == 'POST':
        print(response.POST)
        form = sheetCreator(response.POST)

        if form.is_valid():
            t = Sheet(name=form.cleaned_data["name"])
            t.save()

        return HttpResponseRedirect('/', {})
    else:
        form = sheetCreator()
        return render(response, "main/create.html", {"form": form})

def allsheets(response):
    t = Sheet.objects.all()
    return render(response, "main/sheets.html", {"sheets": t})
