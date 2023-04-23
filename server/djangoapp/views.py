from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from . import restapis
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
import requests
from django.http import JsonResponse
from .models import CarModel,CarDealer,CarMake

# Get an instance of a logger
logger = logging.getLogger(__name__)

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
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/f531064e-b99e-4139-b829-b8a7b8d85715/dealership-package/get_dealer_list.json"
        # Get dealers from the URL
        dealerships = restapis.get_dealers_from_cf(url)
        # Concat all dealer's short name
        context = {'dealerships': dealerships}
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)


#look the specific dealer information
def get_dealer_id(request,dealer_id):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/f531064e-b99e-4139-b829-b8a7b8d85715/dealership-package/dealergetbyid.json"
        # Get dealers from the URL
        dealer = restapis.get_dealer_by_id(url,dealer_id)
        return dealer


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request,dealer_id):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/f531064e-b99e-4139-b829-b8a7b8d85715/review-package/give_review_dealer.json"
        # Get dealers from the URL
        context = {}
        dealer = get_dealer_id(request,dealer_id)
        reviews = restapis.get_dealer_reviews_from_cf(url,dealer_id)
        if dealer:
            context["dealer"] = dealer
            context["reviews"] = reviews
        #the reviews here is dictionary
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request,dealer_id):
#     #this should be switch later
#     if request.method == "POST":         
#         # review = {}
#         # review["time"] = datetime.utcnow().isoformat()
#         # review["dealership"] = dealer_id
#         # review["name"] = request.user.name
#         # review["review"] = request.POST.get("review")
#         # review["purchase"] = request.POST.get("purchase")
#         json_payload = {}
#         #json_payload["review"] = review
#         url = "https://eu-de.functions.appdomain.cloud/api/v1/web/f531064e-b99e-4139-b829-b8a7b8d85715/review-package/addreview_seq.json"
#         response = restapis.post_request(url, json_payload = json_payload)
#         return render(request, 'djangoapp/add_review.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    dealer = get_dealer_id(request,dealer_id)

    # Handle GET request
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = {
            'dealer_id': dealer_id,
            'dealer': dealer,
            'cars': cars,
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        content = request.POST.get('content')
        purchase_check = request.POST.get('purchasecheck') == 'on'
        car_id = request.POST.get('car')
        car = CarModel.objects.get(pk=car_id)
        car_make = car.car_make.name
        car_model = car.name
        car_year = car.year.strftime('%Y')
        purchase_date = request.POST.get('purchasedate')
        # Create a JSON payload with the data
        json_payload = {
            'name': request.user.username,
            'dealership': dealer_id,
            'review': content,
            'purchase': purchase_check,
            'purchase_date': purchase_date,
            'car_make': car_make,
            'car_model': car_model,
            'car_year': car_year
        }

        # Send the payload to the server
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/f531064e-b99e-4139-b829-b8a7b8d85715/review-package/addreview_seq.json"
        response = restapis.post_request(url, json_payload=json_payload)

        if response.get("error"):
            messages.error(request, 'There was an error submitting your review.')
        else:
            messages.success(request, 'Your review has been submitted successfully!')
            print("post sucess")
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
            
            
    return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id})
