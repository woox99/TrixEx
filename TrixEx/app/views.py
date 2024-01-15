# app/views/user.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

import bcrypt

from .models import User, ExampleProject, Project

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
        return redirect('/TrixEx.com/home')

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
        return redirect('/TrixEx.com/home')
    
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
    return redirect('/TrixEx.com/home')

# HOME
# Displays home page
def home(request):
    if 'userId' not in request.session:
        return redirect('/TrixEx')
    user = User.objects.get(id=request.session['userId'])
    # Get all public projects to display on home page
    projects = Project.objects.filter(is_public=1).order_by('-created_at')

    # Create sets for bookmarks and likes for BigO(1) lookup
    bookmarked_projectIds_set = set()
    bookmarked_projects = user.bookmarked_projects.all()
    for project in bookmarked_projects:
        bookmarked_projectIds_set.add(project.id)
    liked_projectIds_set = set()
    liked_projects = user.liked_projects.all()
    for project in liked_projects:
        liked_projectIds_set.add(project.id)

    context = {
        'user' : user,
        'projects' : projects,
        'bookmarked_projectIds_set' : bookmarked_projectIds_set,
        'liked_projectIds_set' : liked_projectIds_set,
    }
    return render(request, 'home.html', context)

# CREATE
# Displays and handles create page
def create(request):
    if request.method == 'GET':
        example = ExampleProject.objects.get(id=1)
        context = {
            'user' : User.objects.get(id=request.session['userId']),
            'example' : example
        }
        return render(request, 'create.html', context)
    if request.method == 'POST':
        title = request.POST['title']
        css = request.POST['css_input']
        html = request.POST['html_input']
        js = request.POST['js_input']
        is_public = request.POST['is_public']
        scale = request.POST['scale']
        margin_top = request.POST['margin_top']
        margin_left = request.POST['margin_left']
        owner = User.objects.get(id=request.session['userId'])
        Project.objects.create(title=title, html=html, css=css, js=js, is_public=is_public, scale=scale, margin_top=margin_top, margin_left=margin_left, owner=owner)
        return redirect('/TrixEx.com/home')

# AJAX CALL
# Bookmark Project
def bookmark(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    if project in user.bookmarked_projects.all():
        user.bookmarked_projects.remove(project)
    else:
        user.bookmarked_projects.add(project)
    return HttpResponse()

# AJAX CALL
# Like Project
def like(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    if project in user.liked_projects.all():
        user.liked_projects.remove(project)
    else:
        user.liked_projects.add(project)
    return HttpResponse()

# BOOKMARKS
# Displays and handles bookmarks page
def bookmarks(request):
    user = User.objects.get(id=request.session['userId'])
    
    # Create sets for bookmarks and likes for BigO(1) lookup
    bookmarked_projectIds_set = set()
    projects = user.bookmarked_projects.all().order_by('bookmarked_users__created_at')[::-1]
    for project in projects:
        bookmarked_projectIds_set.add(project.id)
    liked_projectIds_set = set()
    liked_projects = user.liked_projects.all()
    for project in liked_projects:
        liked_projectIds_set.add(project.id)

    context = {
        'user' : user,
        'projects' : projects,
        'bookmarked_projectIds_set' : bookmarked_projectIds_set,
        'liked_projectIds_set' : liked_projectIds_set,
    }
    return render(request, 'bookmarks.html', context)

# VIEW
# Displays and handles view page
def view(request, project_id):
    project = Project.objects.get(id=project_id)
    context = {
        'user' : User.objects.get(id=request.session['userId']),
        'project' : project
    }
    return render(request, 'view.html', context)

# FOLDER
# Displays and handles folder page
def folder(request, folder_userId, username):
    # If viewing own folder, user & folder_user will be same
    user = User.objects.get(id=request.session['userId'])
    folder_user = User.objects.get(id=folder_userId)
    
    # If viewing own folder, get all projects, else get public projects 
    if folder_userId == user.id:
        projects = Project.objects.filter(owner_id=folder_userId).order_by('-created_at')
    else:
        projects = Project.objects.filter(owner_id=folder_userId, is_public=1).order_by('-created_at')

    # Create sets for bookmarks, likes, and followings for BigO(1) lookup
    bookmarked_projectIds_set = set()
    bookmarked_projects = user.bookmarked_projects.all()
    for project in bookmarked_projects:
        bookmarked_projectIds_set.add(project.id)
    liked_projectIds_set = set()
    liked_projects = user.liked_projects.all()
    for project in liked_projects:
        liked_projectIds_set.add(project.id)
    following_userIds_set = set()
    following = user.following.all()
    for followee in following:
        following_userIds_set.add(followee.id)

    context = {
        'user' : user,
        'folder_user' : folder_user,
        'projects' : projects,
        'bookmarked_projectIds_set' : bookmarked_projectIds_set,
        'liked_projectIds_set' : liked_projectIds_set,
        'following_userIds_set' : following_userIds_set,
    }

    return render(request, 'folder.html', context)


# AJAX  CALL
# Get all public projects (home page)
def getAll(request):
    projects = Project.objects.filter(is_public=1)
    
    # Serialize the projects to JSON
    serialized_projects = []
    for project in projects:
        serialized_projects.append({
            'id' : project.id,
            'html': project.html,
            'css': project.css,
            'js': project.js,
            'scale': project.scale,
            'margin_top': project.margin_top,
            'margin_left': project.margin_left,
        })
    return JsonResponse(serialized_projects, safe=False)

# AJAX  CALL
# Get all projects by user (folder page)
def getAllByUser(request, userId):
    if userId == request.session['userId']:
        projects = Project.objects.filter(owner_id=userId)
    else:
        projects = Project.objects.filter(owner_id=userId, is_public=1)

    # Serialize the projects to JSON
    serialized_projects = []
    for project in projects:
        serialized_projects.append({
            'id' : project.id,
            'html': project.html,
            'css': project.css,
            'js': project.js,
            'scale': project.scale,
            'margin_top': project.margin_top,
            'margin_left': project.margin_left,
        })
    return JsonResponse(serialized_projects, safe=False)

# AJAX CALL
# Get all bookmarked projects (bookmarks page)
def getBookmarks(request):
    user = User.objects.get(id=request.session['userId'])
    projects = user.bookmarked_projects.all()
    
    # Serialize the projects to JSON
    serialized_projects = []
    for project in projects:
        serialized_projects.append({
            'id' : project.id,
            'html': project.html,
            'css': project.css,
            'js': project.js,
            'scale': project.scale,
            'margin_top': project.margin_top,
            'margin_left': project.margin_left,
        })
    return JsonResponse(serialized_projects, safe=False)

# AJAX CALL
# Follow followee
def follow(request, followeeId):
    user = User.objects.get(id=request.session['userId'])
    followee = User.objects.get(id=followeeId)

    if followee in user.following.all():
        user.following.remove(followee)
    else:
        user.following.add(followee)
    return HttpResponse()