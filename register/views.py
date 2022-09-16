from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
# function that creates new user account
def register(response):
    if response.method == 'POST':
        new_user = UserCreationForm(response.POST)

        if new_user.is_valid():
            new_user.save()

        return redirect('/')

    else:
        form = UserCreationForm()

    return render(response, 'register/register.html', {"form": form})