import email
import ast
from itertools import product
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from accounts.forms import RegistrationForm, UserAuthenticationForm, ProfileEdit, UserChangeForm
from .models import Product, Cart

def registration_view(request):
    context = {}
    if request.POST:
        print("Inside Registration")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            #TODO: why are we authenticating during signup?
            # account = authenticate(username=username, password = raw_password)
            # login(request,account)
            return redirect('login')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'registration/register.html',context)

# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user.user_type=='patient':
                    login(request,user)
                    return redirect("patient_index")
                    
                
            # elif user.user_type==''

    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request,'registration/login.html',context)


def editprofile(request):
    context = {}
    
    user=request.user
    if not user.is_authenticated:
        return redirect('login')
    
    if request.POST:
        form=ProfileEdit(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        
    else:
        form = ProfileEdit(initial={"email":request.user.email, "username":request.user.username,
                                    "official_name":request.user.official_name,"mobile":request.user.mobile,
                                    "user_type":request.user.user_type,
                                    "address":request.user.address})
    

    context['edit_form']= form
    return render(request, 'registration/edit.html',context)
    
    def get_object(self):
        return self.request.user
    
    
def patient_view(request):
    
    return render(request, 'patient_index.html')   

def cart(request):
    productsss = Product.objects.all()
    #  print(productsss.values)
    #  print(request.POST)

    if request.POST:
        res = request.POST
        products_dict = {}
        for i in productsss:
            products_dict[i.id] = {'quantity':res[i.name], 'cost_per_medicine':i.price}
        print(products_dict)
        amount = add_to_cart(products_dict)
    else:
        return render(request, 'patient_index.html',{'products':productsss})

    return redirect(f'/payments/views/homepage?amount={amount}', amount=amount)
    
    # return render(request, 'payments_template/payment_success.html', {'amount':amount})
    
    

def add_to_cart(cart_dict):
    amount=0
    for k,v in cart_dict.items():
        # item = Cart(product=k, quantity=v)
        amount+=ast.literal_eval(v['quantity'])*v['cost_per_medicine']
        print(amount)
        item = Cart(product=k, quantity=v['quantity'], amount=amount)
        item.save()
    return amount




   
    


