# app/views/user.py
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import User

# INDEX
# Validates and creates user registration
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    # Register user if POST
    if request.method == 'POST':
        # Validate registration
        errors = User.objects.validate_register(request.POST)

        # If registration not valid return errors
        if len(errors) > 0:
            form_data = {
                'username' : request.POST['username'],
                'email' : request.POST['email'],
                'password' : request.POST['password']
            }
            context = {**errors, **form_data}
            return render(request, 'register.html', context)
        
        # If registration is valid, create user and store ID in session
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(email=email, username=username, password=pw_hash)
        request.session['userId'] = user.id
        return redirect('/TrixEx/home')

# LOGIN
# Validates and handles user login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)

        # If login is not valid, return errors
        if len(errors) > 0:
            form_data = {
                'email' : request.POST['email'],
                'password' : request.POST['password'],
            }
            context = {**form_data, **errors}
            return render(request, 'login.html', context)
        # If login is valid, get user and store ID in session
        user = User.objects.get(email=request.POST['email'])
        request.session['userId'] = user.id
        print(user.id)
        return redirect('/TrixEx/home')
    
# LOGOUT
# Displays and handles logout
def logout(request):
    user = User.objects.get(id=request.session['userId'])
    del request.session['userId']
    context = {
        'username' : user.username
    }
    return render(request, 'logout.html', context)

# DEMO ACCOUNT
# Creates demo account
def demo(request):
    id = User.objects.all().last().id + 1
    username = 'DemoAccount#' + str(id)
    email = 'demo'
    is_demo = True
    demo = User.objects.create(username=username, is_demo=is_demo, email=email)
    request.session['userId'] = demo.id
    return redirect('/TrixEx/home')

# HOME
# Displays home page
def home(request):
    if 'userId' not in request.session:
        return redirect('/TrixEx')
    user = User.objects.get(id=request.session['userId'])
    context = {
        'user' : user
    }
    return render(request, 'home.html', context)

# Create
# Displays and handles create page
def create(request):
    return render(request, 'create.html')
