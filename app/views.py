import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import *


def index(request):
    return render(request, 'index.html')

def register_user(request):

    errors = User.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt() 
        ).decode() 
    
        print(hash_browns)
    
        created_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            hashed_password=hash_browns,
        )
        request.session['emailid'] = created_user.id

        return redirect('/quotes')


def login_user(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['emailid'] = user.id
        return redirect('/quotes')


def logout_user(request):
    del request.session['emailid']
    return redirect('/')

def show_quotes(request):
    if 'emailid' not in request.session:
        return redirect('/')
    context = {
        'user_logged_in': User.objects.get(id=request.session['emailid']),
        'quotes': Quote.objects.all(),
        'total_likes_received' : Quote.objects.filter(like=request.session['emailid']).count()
        
    }
    return render(request, 'quotes.html', context)

def create_quote(request):
    errors = Quote.objects.quote_validator(request.POST)

    if len(errors) > 0:
   		for key, value in errors.items():
   			messages.error(request, value)
   		return redirect('/quotes')

    else:
        logged_in_user = User.objects.get(id=request.session['emailid'])
        new_created_quote = Quote.objects.create(
            author = request.POST['author'],
            desc = request.POST['desc'],
            maker = logged_in_user
        )
        return redirect('/quotes')

def user_edit(request, email_id):
    context = {
        'userEdit': User.objects.get(id=email_id)
    }
    return render(request, 'user_edit.html', context)


def user_update(request, email_id):
	
    errors = User.objects.edit_validator(request.POST)
    
    if len(errors) > 0:
        
        for key, value in errors.items():
            print(key, value)
            messages.error(request, value)
        return redirect(f'/quotes/edit/{email_id}')
    else:
        user_to_update = User.objects.get(id=email_id)
        user_to_update.first_name = request.POST['first_name']
        user_to_update.last_name = request.POST['last_name']
        user_to_update.email = request.POST['email']
        user_to_update.save()
        return redirect(f'/quotes')

def user_quotes(request, email_id):
    context = {
        'userQuotes': Quote.objects.filter(maker_id=email_id)
    }
    return render(request, "userDetails.html", context)

def mark_quote_as_like(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['emailid'])
    user.liked.add(quote)
    return redirect('/quotes')

def mark_quote_as_unlike(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['emailid'])
    user.liked.remove(quote)
    return redirect('/quotes')

def quote_destroy(request, quote_id):
    Quote.objects.get(id=quote_id).delete()
    return redirect('/quotes')
