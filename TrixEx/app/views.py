# app/views/user.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q


import bcrypt

from .models import User, Project, Comment, Reply

# INDEX
# Validates and creates user registration
def index(request):
    if request.method == 'GET':
        projects = Project.objects.filter(is_landing=1)
        context = {
            'projects' : projects,
        }
        return render(request, 'index.html', context)
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
        return redirect('/TrixEx.com/home')
    
# LOGOUT
# Displays and handles logout
def logout(request):
    user = User.objects.get(id=request.session['userId'])
    del request.session['userId']
    context = {
        'username' : user.username
    }
    return redirect('/TrixEx.com')

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
        return redirect('/TrixEx.com')
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
        example = Project.objects.get(is_example=True)
        context = {
            'user' : User.objects.get(id=request.session['userId']),
            'example' : example
        }
        return render(request, 'create.html', context)
    if request.method == 'POST':
        user = User.objects.get(id=request.session['userId'])
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
        return redirect(f'/TrixEx.com/folder{user.id}/{user.username}')

# Edit Project
# Displays and handles create page
def edit(request, projectId):
    if request.method == 'GET':
        example = Project.objects.get(is_example=True)
        context = {
            'user' : User.objects.get(id=request.session['userId']),
            'example' : example
        }
        return render(request, 'edit.html', context)
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


# BOOKMARKS
# Displays and handles bookmarks page
def bookmarks(request):
    user = User.objects.get(id=request.session['userId'])
    
    # Create sets for bookmarks and likes for BigO(1) lookup
    projects = user.bookmarked_projects.all().order_by('bookmarked_users__created_at')[::-1]
    bookmarked_projectIds_set = set()
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

# SEARCH
# Displays search page
def search(request):
    user = User.objects.get(id=request.session['userId'])
    
    # Create sets for bookmarks and likes for BigO(1) lookup
    searchKey = request.POST['searchKey']
    projects = Project.objects.filter(Q(title__icontains=searchKey) | Q(owner__username__icontains=searchKey), is_public = True)
    bookmarked_projects = user.bookmarked_projects.all()
    bookmarked_projectIds_set = set()
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
        'searchKey' : searchKey,
    }
    return render(request, 'search.html', context)

# VIEW
# Displays and handles view page
def view(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    project.views += 1
    project.save()
    comments = project.comments.all().order_by('-created_at')

    # Create sets for bookmarks and likes for BigO(1) lookup
    bookmarked_projectIds_set = set()
    bookmarked_projects = user.bookmarked_projects.all()
    for bookmarked_project in bookmarked_projects:
        bookmarked_projectIds_set.add(bookmarked_project.id)
    liked_projectIds_set = set()
    liked_projects = user.liked_projects.all()
    for liked_project in liked_projects:
        liked_projectIds_set.add(liked_project.id)
    liked_commentIds_set = set()
    liked_comments = user.liked_comments.all()
    for liked_comment in liked_comments:
        liked_commentIds_set.add(liked_comment.id)
    following_userIds_set = set()
    following = user.following.all()
    for followee in following:
        following_userIds_set.add(followee.id)

    context = {
        'user' : user,
        'project' : project,
        'bookmarked_projectIds_set' : bookmarked_projectIds_set,
        'liked_projectIds_set' : liked_projectIds_set,
        'liked_commentIds_set' : liked_commentIds_set,
        'following_userIds_set' : following_userIds_set,
        'comments' : comments,
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

# Create Comment
def comment(request, projectId):
    owner = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    content = request.POST['content']
    Comment.objects.create(owner=owner, project=project, content=content)
    return redirect(f'/TrixEx.com/view/{projectId}#commentSection')

# Create Reply
def reply(request, commentId):
    owner = User.objects.get(id=request.session['userId'])
    comment = Comment.objects.get(id=commentId)
    content = request.POST['content']
    Reply.objects.create(owner=owner, comment=comment, content=content)
    return redirect(f'/TrixEx.com/view/{comment.project.id}#commentSection')

# Update Motto
def updateMotto(request):
    user = User.objects.get(id=request.session['userId'])
    user.motto = request.POST['motto']
    user.save()
    return redirect(f'/TrixEx.com/folder{user.id}/{user.username}')

def deleteProject(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    project.delete()
    return redirect(f'/TrixEx.com/folder{user.id}/{user.username}')

def deleteComment(request, commentId):
    comment = Comment.objects.get(id=commentId)
    comment.delete()
    return redirect(f'/TrixEx.com/view/{comment.project.id}#commentSection')

def deleteReply(request, replyId):
    reply = Reply.objects.get(id=replyId)
    reply.delete()
    return redirect(f'/TrixEx.com/view/{reply.comment.project.id}#commentSection')


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
# Get all landing projects (index page)
def getAllLanding(request):
    projects = Project.objects.filter(is_landing=1)
    
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
# Get search result projects (search page)
def getSearchProjects(request, searchKey):
    user = User.objects.get(id=request.session['userId'])
    projects = Project.objects.filter(Q(title__icontains=searchKey) | Q(owner__username__icontains=searchKey), is_public = True)
    
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
def likeProject(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    if project in user.liked_projects.all():
        user.liked_projects.remove(project)
    else:
        user.liked_projects.add(project)
    return HttpResponse()

# AJAX CALL
# Like Comment
def likeComment(request, commentId):
    user = User.objects.get(id=request.session['userId'])
    comment = Comment.objects.get(id=commentId)
    if comment in user.liked_comments.all():
        user.liked_comments.remove(comment)
    else:
        user.liked_comments.add(comment)
    return HttpResponse()

# AJAX CALL
# Visibility Toggle
def visibility(request, projectId):
    user = User.objects.get(id=request.session['userId'])
    project = Project.objects.get(id=projectId)
    if project.is_public == 1:
        project.is_public = 0
        project.save()
    else:
        project.is_public = 1
        project.save()
    return HttpResponse()