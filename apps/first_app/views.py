from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

def index(request):
    return render(request, 'first_app/index.html')

def processreg(request):
    result = User.objects.validate_registration(request.POST)
    if result['status']:    #that means if its true
        request.session['user_id'] = result['user_id']
        return redirect('/quotes')
    else:
        for error in result['errors']:
            messages.error(request,error)   
    return redirect('/')


def processlog(request):
    result = User.objects.validate_login(request.POST)
    if result['status']: #that means if its true
        request.session['user_id'] = result['user_id']
        return redirect('/quotes')
    else:
        for error in result['errors']:
            messages.error(request,error)    
    return redirect('/')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect('/')

    context ={
        "me": User.objects.get(id=request.session['user_id']),
        'users': User.objects.all(),
        "all_quotes": Quote.objects.all(),
        "not_my_quotes": Quote.objects.exclude(others=request.session['user_id']),
        "my_quotes": Quote.objects.filter(others=request.session['user_id'])

    }
    return render(request, 'first_app/quotes.html', context)
def submit(request):
    result = Quote.objects.validate_submit(request.POST, request.session['user_id'])
    if result['status']:   
        return redirect('/quotes')
    else:
        for error in result['errors']:
            messages.error(request,error)   
    return redirect('/quotes')

def posted_others(request,user_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context ={
        'user' : User.objects.get(id=user_id),
        'my_quotes': Quote.objects.filter(posted_by=user_id)
    }

    return render(request,'first_app/info.html',context)

def add(request, quote_id):
    Quote.objects.add(quote_id, request.session['user_id'])
    return redirect('/quotes')

def remove(request, quote_id):
    Quote.objects.remove(user_id=request.session['user_id'],quote_id=quote_id)
    return redirect('/quotes')

def home(request):
    return redirect('/quotes')
   
def logout(request):
    request.session.flush() 
    return redirect('/')