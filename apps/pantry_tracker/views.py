from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime, date, time
import datetime
from .models import *
import re, bcrypt

def landing(request):
    response = "Landing Page"
    print("///////////////////////////////////////////////////////////////////////////////////////////////////")
    print("Remaining time left until item is spoiled")
    print("///////////////////////////////////////////////////////////////////////////////////////////////////")
    timeToSpoil = ""
    for product in Product.objects.filter(pantry = Pantry.objects.get(id = User.objects.get(id = 1).id)): 
        ItemBoughtAt = Product.objects.get(id = product.id).created_at.strftime("%d")
        today = datetime.date.today().strftime("%d")
        #Update id = 1 to 1 = request.session['user_id']
        if product.shelf_life:
            if product.created_at.strftime("%m") != datetime.date.today().strftime("%m"):
                ItemBoughtAt = datetime.date.today().strftime("%m")
                timeToSpoil = timeToSpoil - 1
            timeToSpoil = Product.objects.get(id = product.id).shelf_life
            timeToSpoil = timeToSpoil - (int(today) - int(ItemBoughtAt))
    print("///////////////////////////////////////////////////////////////////////////////////////////////////")
    return HttpResponse(response)

def login(request):
    return render(request, 'login.html')

def loginUser(request):
    return redirect('/dashboard') 

def register(request):
    return render(request, 'register.html')

def registerUser(request):
    return redirect('/dashboard') 

def dashboard(request):
    return render(request, 'dashboard.html')

def profile(request):
    # Needs an user id number
    response = "Profile Page"
    return HttpResponse(response)

def editProfile(request):
    # Needs an user id number
    response = "Edit Profile"
    return HttpResponse(reponse)

def shoppingList(request):
    # Needs an user id number
    response = "Shopping List"
    return HttpResponse(response)

def editShoppingList(request):
    # Needs an user id number
    # needs a shoppingList id ?????
    response = "Shopping List"
    return HttpResponse(response)

def products(request):
    response = "All Products available"
    return HttpResponse(response)

def viewProduct(request):
    # Needs a product id number
    response = "Current Product"
    return HttpResponse(response)

def myPantry(request):
    # Needs an user id number
    response = "My Pantry"
    return HttpResponse(response)

def editPantry(request):
    # Needs an user id number
    response = "My Pantry"
    return HttpResponse(response)

def logout(request):
    # del request.session['user_id']
    return redirect('/')


# **************************************************************************************************************************
# ******************************BELOW IS THE VALIDATIONS WE WILL BE EDITING AND USING***************************************
# **************************************************************************************************************************



# def login(request):
#     return(request, 'login.html')

# def login(request):
#     errors = User.objects.login_validator(request.POST)
#     if len(errors):
#         for tag, error in errors.items():
#             messages.error(request, error, extra_tags = tag)
#         return redirect('/')
#     else:
#         request.session['user_id'] = User.objects.get(email=request.POST['loginEmail']).id
#         return redirect('/dashboard')

# def register(request):
#     errors = User.objects.registrator_validator(request.POST)
#     if len(errors):
#         for tag, error in errors.items():
#             messages.error(request, error, extra_tags = tag)
#         return redirect('/')
#     else:
#         user = User.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
#         request.session['user_id'] = user.id
#         return redirect('/dashboard')
   
# def index(request):
#     request.session['servercheck'] = "Success!"
#     return render(request, 'index.html')



# def dashboard(request):
#     if 'user_id' not in request.session:
#         return redirect('/')
#     else:
#         user = User.objects.get(id=request.session['user_id'])
#         context = {
#             'id': user.id,
#             'first_name':user.first_name,
#             'last_name':user.last_name,
#             'email': user.email
#         }
#     return render(request,'dashboard.html', context)
