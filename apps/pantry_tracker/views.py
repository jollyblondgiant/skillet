from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Validator
import re, bcrypt
def index(request):
    request.session['servercheck'] = "Success!"
    return render(request, 'index.html')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['loginEmail']).id
        return redirect('/dashboard')

def register(request):
    errors = User.objects.registrator_validator(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        user = User.objects.create(first_name = request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = user.id
        return redirect('/dashboard')
   

def logout(request):
    del request.session['user_id']
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'id': user.id,
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email': user.email
        }
    return render(request,'dashboard.html', context)
# Create your views here.
