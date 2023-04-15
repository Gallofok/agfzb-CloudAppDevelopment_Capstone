from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('djangoapp:index')
    else:
        form = AuthenticationForm()
    return render(request, 'djangoapp/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def signup_request(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # log in the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('djangoapp:index')        
    else:
        form = UserCreationForm()
    return render(request, 'djangoapp/registration.html', {'form': form})

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

