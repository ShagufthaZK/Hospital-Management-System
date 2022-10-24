from django.shortcuts import render, HttpResponse, redirect

from home.models import Contact
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login

# Create your views here.

def index(request):
    context ={
        'variable':'this is sent'
    }   
    
    return render(request,'index.html', context)

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            return redirect("/")

        else:
            # No backend authenticated the credentials
            return render(request, 'login.html')
    return render(request,'login.html')
    
def logoutUser(request):
    logout(request)
    
    return redirect("/login")

def about(request): 
    return render(request,'about.html')
    #return HttpResponse("This is about page")

def service(request):
    return render(request,'services.html')
    # return HttpResponse("This is service page")
    
def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=Contact(name=name,email=email)
        contact.save()
        messages.success(request, 'Sign up completed')
    return render(request,'contact.html')
    # return HttpResponse("This is service page")
