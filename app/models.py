from __future__ import unicode_literals
from datetime import datetime, timedelta
import bcrypt
import re
from django.db import models

email_characters = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
name_characters = re.compile(r"^[a-zA-Z-']+$")

class UserManager(models.Manager):
    def register_validator(self, post_data):
        errors = {}
        
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be longer than 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be longer than 2 characters'

        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be longer than 8 characters'

        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Password does not match'

        if not name_characters.match(post_data['first_name']):
            errors['first_name'] = "Invalid characters in First Name"

        if not name_characters.match(post_data['last_name']):
            errors['last_name'] = "Invalid characters in Last Name"

        if not email_characters.match(post_data['email']):
            errors['email'] = "Invalid Email Address"

        if len(User.objects.filter(email = post_data['email'])) > 0:
            errors['email'] = "Email already exists"

        return errors


    def login_validator(self, post_data):
        errors = {}

        emails_list = User.objects.filter(email=post_data['email'])

        if not email_characters.match(post_data['email']):
            errors['email'] = "Invalid Email Address"

        if len(emails_list) == 0:
            errors['email'] = "Email does not exist"

        elif not bcrypt.checkpw(post_data['password'].encode(), emails_list[0].hashed_password.encode()):
            errors['password'] = 'Password did not match'
        return errors

    def quote_validator(self, post_data):
        errors = {}
        
        if len(post_data['author']) < 3:
            errors['author'] = ' Author Name must be longer than 3 characters'

        if len(post_data['desc']) < 10:
            errors['desc'] = 'Desc  must be longer than 10 characters'

        return errors

    def edit_validator(self, post_data):
        errors = {}
        
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name must be longer than 2 characters'

        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name must be longer than 2 characters'

        if not name_characters.match(post_data['first_name']):
            errors['first_name'] = "Invalid characters in First Name"

        if not name_characters.match(post_data['last_name']):
            errors['last_name'] = "Invalid characters in Last Name"

        if not email_characters.match(post_data['email']):
            errors['email'] = "Invalid Email Address"

        if len(User.objects.filter(email = post_data['email'])) > 0:
            errors['email'] = "Email already exists"

        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    hashed_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author= models.CharField(max_length=100)
    desc= models.TextField(max_length=1000)
    maker= models.ForeignKey(User, related_name= "quoter", on_delete=models.CASCADE)
    like= models.ManyToManyField(User, related_name="liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()