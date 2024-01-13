from django.db import models

import re
import bcrypt

class UserManager(models.Manager):
    def validate_register(self,data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9]+$')

        if len(data['username']) < 3:
            errors["username_error"] = "Username must be between 4-12 characters."
        if not USERNAME_REGEX.match(data['username']):
            errors['username_error'] = 'Username must be letters and numbers only.'
        if len(data['username']) == 0:
            errors["username_error"] = "Please create a username."
        if not EMAIL_REGEX.match(data['email']):
            errors['email_error'] = 'Invalid email'
        if len(data['email']) == 0:
            errors['email_error'] = 'Please enter your email.'
        if len(data['password']) < 3:
            errors['password_error'] = 'Password must be a least 3 characters.'
        if len(data['password']) == 0:
            errors['password_error'] = 'Please create a password.'
        if User.objects.filter(email=data['email']).exists():
            errors['email_error'] = 'This email already has an account.'
        if User.objects.filter(username=data['username']).exists():
            errors['username_error'] = 'This username is unavailable.'

        return errors
    
    def validate_login(self, data):
        errors = {}
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            errors['email_error'] = 'Invalid email.'
            return errors
        
        if not bcrypt.checkpw(data['password'].encode(), user.password.encode()):
            errors['password_error'] = 'Incorrect password.'
        return errors

class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=12)
    password = models.TextField()
    is_demo = models.BooleanField(default=False)
    # is_admin = models.BooleanField()
    # is_authorized = models.BooleanField()
    # is_banned = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager() 
    # Projects

class ExampleProject(models.Model):
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Project(models.Model):
    owner = models.ForeignKey(User, related_name="projects", on_delete = models.CASCADE)
    title = models.CharField(max_length=16)
    html = models.TextField()
    css = models.TextField()
    js = models.TextField()
    is_public = models.BooleanField()
    scale = models.FloatField()
    margin_top = models.FloatField()
    margin_left = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)