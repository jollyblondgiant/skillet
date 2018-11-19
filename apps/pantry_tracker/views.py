from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import re, bcrypt

#Where we start. If logged in will redirect to dash
#If not logged in - redirect to log in/register view
def landing(request):
    if 'current_user' in request.session:
        return redirect('/dashboard')
    else:
        return render(request,"landing.html")

#Logout wipes the session out, dumps user back to landing
def logout(request):

    request.session.clear()
    return redirect('/')

#This is the view for showing a login window with the form
#By default, this will be the first thing a new user sees
def login(request):
    return render(request, 'login.html')

#View for processing the actual user login
def loginUser(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect('/login')
        else:
            email = request.POST['loginEmail']
            user = User.objects.get(email=email)
            request.session['user_id'] = user.id
            access_level = user.access_level
            print("&"*80)
            print(user.__dict__)
            #check if the user logging in is the admin
            if access_level == 9 or access_level == 7:
                print("Going to ADMIN")
                return redirect('/admin_dash')
            else:
                print("Going to userr")
                return redirect('/dashboard')
    return redirect('/dashboard') 

#Render registration form
def register(request):
    return render(request, 'register.html')

#Process registration
def registerUser(request):
    if request.method == 'POST':
        errors = User.objects.registrator_validator(request.POST)
        if len(errors):
            for tag, error in errors.items():
                messages.error(request, error, extra_tags = tag)
            return redirect('/')
        else:
            #new addition, for establishing admins
            #admins will be able to promote others
            if User.objects.all().count()==0:
                access_level = 9
            elif 'access_level' in request.POST:
                access_level=request.POST['access_level']
            else:
                access_level = 1
            #Make an empty pantry for the new user
            pantry = Pantry.objects.create()
            user = User.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()),access_level=access_level, pantry=pantry)

            request.session['user_id'] = user.id
            if user.access_level==9 or user.access_level==7:
                return redirect('/admin_dash')
    return redirect('/dashboard')

def user_delete(request,id):
    user = User.objects.get(id=id)
    if user.access_level == 1:
        user.delete()
    else:
        print('!-'*88)
        print("Can't delete admins!!!")
    return redirect('/admin_dash')

#User main page - all the content except profile editing
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user=User.objects.get(id=request.session['user_id'])
    name=user.first_name+" "+user.last_name
    pantrylist=[]
    for product in user.pantry.product.order_by('name'):
        temp={
            'name':product.name,
            'id':product.id,
            'img':product.image,
            'time':12
        }
        pantrylist.append(temp)
    context = {
        'username':name,
        'access_level': user.access_level,
        'pantrylist':pantrylist,
    }
    return render(request, 'dashboard.html',context)
#**********************************************************

# Take user to the page for profile editing
def editProfile(request,id):
    context = {}
    return render(request,"edit.html", context)

# Processes whatever changes the users submits
def update_profile(request,id):
    return redirect('/dashboard') 
#**********************************************************

def myPantry(request):
    # Needs an user id number
    response = "My Pantry"
    return render(request,"user-templates/pantry.html", context)

def editPantry(request):
    # Needs an user id number
    response = "My Pantry"
    return redirect('/myPantry')
#**********************************************************

# Needs an user id number
def shoppingList(request):
    response = "Shopping List"
    return HttpResponse(response)

def editShoppingList(request):
    # Needs an user id number
    # needs a shoppingList id ?????
    response = "Shopping List"
    return HttpResponse(response)
#**********************************************************

def admin_dash(request):
    u=User.objects.get(id=request.session['user_id'])
    if u.access_level == 1:
        return redirect('/dashboard')
    userlist = []
    for user in User.objects.all():
        temp = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            'access_level':user.access_level,
            'pantry':user.pantry.id,
        }
        userlist.append(temp)
    productlist=[]
    for product in Product.objects.all():
        temp = {
            'id': product.id,
            'name':product.name,
            'desc':product.description,
            'quantity':product.quantity,
            'unit':product.measure,
            'shelf_life':product.shelf_life,
            'price':product.price,
            'owner':product.pantry.user.first().first_name,
        }
        productlist.append(temp)
    recipelist=[]
    for recipe in Recipe.objects.all():
        #this is you, the admin
        author = recipe.author.first_name + " " + recipe.author.last_name
        temp = {
            'id': recipe.id,
            'name':recipe.name,
            'desc':recipe.desc,
            'author': author,
            'author_id':recipe.author.id
        }
    context = {
        'userlist':userlist,
        'productlist':productlist,
        'recipelist':recipelist,
        'adminname':u.first_name
    }

    return render(request,"admin-templates/admin-dash.html",context)

def add_product(request):
    if request.method == 'POST':
        errors = {}
        if len(errors):
            print(errors)
        else:
            price=request.POST['price']
            Product.objects.create(name=request.POST['name'], description=request.POST['desc'],measure=request.POST['unit'],shelf_life=request.POST['shelf_life'],quantity=1, price=price, pantry=Pantry.objects.get(id=1),image='flour.jpg')
            #NOTE!! This is making products in Andy's pantry. SUBJECT TO CHANGE
    return redirect('/admin_dash')

def recipe_builder(request):
    if 'recipe' not in request.session:
        print('^'*80)
        request.session['recipe']={
            'name':'',
            'desc':'',
            'components':{}
        }
    productlist=[]
    for product in Product.objects.all():
        temp = {
            'id': product.id,
            'name':product.name,
            'desc':product.desc,
            'unit':product.unit,
            'shelf_life':product.shelf_life,
            'price':product.price
        }
        productlist.append(temp)
    context = {
        'productlist':productlist
    }
    return render(request,"admin-templates/recipe_editor.html",context)

#GAAAAAH!!!! What am I doing wrong?
def add_to_recipe(request):
    if request.method == 'POST':
        product_id=request.POST['id']
        print(product_id)
        quantity=int(request.POST['quantity'])
        print(quantity)
        print('Session recipe:')
        print(request.session['recipe'])
        if product_id not in request.session['recipe']['components']:
            print('product id not in session')
            request.session['recipe']['components'][product_id]=quantity
        else:
            request.session['recipe']['components'][product_id]+=quantity
        print("*"*80)
        print(request.session['recipe'])
    return redirect('/recipe_builder')

def recipe_clear(request):
    print("#"*80)
    print('recipe clear')
    request.session['recipe']={
            'name':'',
            'desc':'',
            'components':{}
        }
    return redirect('/recipe_builder')

def complete_recipe(request):
    return redirect('/admin_dash')


#render shopping list page
def shopping_list(request):
    context={}
    return render(request,"grocery.html",context)

def add_groceries(request):
    return redirect('shopping_list')

def done_shopping(request):
    return redirect('dashboard')

# def index(request):
#     request.session['servercheck'] = "Success!"
#     return render(request, 'index.html')
    # del request.session['user_id']
   # return redirect('/')


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
   
# def logout(request):
#     del request.session['user_id']
#     return redirect('/')
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

