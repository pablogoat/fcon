from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from .forms import sheetCreator

# Create your views here.

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == 'POST':
        print(response.POST)
        return HttpResponseRedirect('/', {})
    else:
        form = sheetCreator()
        return render(response, "main/create.html", {"form": form})
