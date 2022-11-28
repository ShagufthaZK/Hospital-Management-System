import email
import ast
from itertools import product
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from accounts.forms import *
# RegistrationForm, UserAuthenticationForm, ProfileEdit, UserChangeForm,AmountForm
from .models import Product, Cart,Symptoms,SymptomsShared,Amount,AmountShared,Insurance,InsuranceShared


import email
# from sms import send_sms
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q

from accounts.models import CustomUser, UserFiles
from .helpers import *
from accounts.forms import *#RegistrationForm, UserAuthenticationForm, ProfileEdit, OTPVerificationForm, OrganizationAndHealthcareProfessionalSearchForm, FileUploadForm

def registration_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
            if user.user_type=='patient':
                    return redirect("patient_index") 
            elif user.user_type=='hospital':
                    return redirect("hospital_index")
            elif user.user_type=='pharmacy':
                    return redirect("pharmacy_index")
            elif user.user_type=='insurance':
                    return redirect("insurance_index")
            else:
                    return redirect("health_prof_index")
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=raw_password)
            #login(request,user)
            #return render(request, 'registration/otp.html',context)
            request.session['username'] = username
            request.session['password'] = raw_password
            #send_otp_email(user)
            return redirect('otp_email')
            #return redirect('login')
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
            if user.user_type=='patient':
                    return redirect("patient_index") 
            elif user.user_type=='hospital':
                    return redirect("hospital_index")
            elif user.user_type=='pharmacy':
                    return redirect("pharmacy_index")
            elif user.user_type=='insurance':
                    return redirect("insurance_index")
            else:
                    return redirect("health_prof_index")
        
    
    if request.POST:
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            #user should not be able to login till email is verified
            if not user.is_email_verified:
                request.session['username'] = username
                request.session['password'] = password
                #send_otp_email(user)
                return redirect("otp_email")

           
            if user.user_type=='patient':
                    #send_otp_email(user)
                    login(request,user)
                    return redirect("patient_index") 
            elif user.user_type=='hospital':
                    login(request,user)
                    return redirect("hospital_index")
            elif user.user_type=='pharmacy':
                    login(request,user)
                    return redirect("pharmacy_index")
            elif user.user_type=='insurance':
                    login(request,user)
                    return redirect("insurance_index")
            else:
                    login(request,user)
                    return redirect("health_prof_index")
            
    else:
        form = UserAuthenticationForm()
    context['login_form'] = form
    return render(request,'registration/login.html',context)

@login_required(login_url='/login/')
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

@login_required(login_url='/login/')
def patient_view(request):
    context = {}
    user=request.user
    if user.user_type != 'patient':
        return redirect('login')
    if request.POST:
        form = OrganizationAndHealthcareProfessionalSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('user_type') == 'all':
                users = CustomUser.objects.filter(official_name__contains=form.cleaned_data.get('name'),address__contains=form.cleaned_data.get('location')).exclude(user_type="patient")
            else:
                users = CustomUser.objects.filter(official_name__contains=form.cleaned_data.get('name'),address__contains=form.cleaned_data.get('location'),user_type = form.cleaned_data.get('user_type')).exclude(user_type="patient")
    else:
        form = OrganizationAndHealthcareProfessionalSearchForm(initial={'user_type':'all'})
        users = CustomUser.objects.exclude(user_type="patient")
        
    context['org_healthcare_profs'] = users
    context['search_form'] = form   
    return render(request, 'patient_index.html',context) 

@login_required(login_url='/login/')
def hospital_view(request):
    context={}
    if request.user.user_type != 'hospital':
        return redirect('login')
    sym=SymptomsShared.objects.filter(shared_to=request.user)#.exclude(completed=True)
    context['sympto']=sym
        
    return render(request, 'hospital_index.html',context) 

@login_required(login_url='/login/')
def healthcare_prof_view(request):
    if request.user.user_type != 'professional':
        return redirect('login')
    sym=SymptomsShared.objects.filter(shared_to=request.user).exclude(completed=True)
    context['sympto']=sym
    return render(request, 'health_index.html',context)

@login_required(login_url='/login/')
def insurance_view(request):
    print('ins entered')
    if request.user.user_type != 'insurance':
        return redirect('login')
    return render(request, 'ins_index.html')


@login_required(login_url='/login/')
def pharmacy_view(request):
    if request.user.user_type != 'pharmacy':
        return redirect('login')
    context = {}
    
    context['pharmacy_requests'] = PharmacyRequest.objects.filter(prescription__shared_to=request.user)#Q(shared_to=request.user)|Q(file__user=request.user))
    print(context)
    return render(request, 'pharmacy_index.html',context)







def otp_email_view(request):
    context = {}
    user=request.user

    # if not user.is_authenticated: 
    #      return redirect('login')

    user = authenticate(username=request.session.get('username'),password=request.session.get('password'))
    if not user:
        return redirect('login')
    if request.POST:
        form = OTPVerificationForm(request.POST, request=request)
        if form.is_valid():
            #form.save()
            #correct = verify_otp_email(user,)
            user.is_email_verified = True
            user.save()
            return redirect('login')
        
    else:
        form = OTPVerificationForm(request=request)
        send_otp_email(user)

    context['otp_form'] = form   
    return render(request,'registration/otp.html',context)

     
@login_required(login_url='/login/')
def show_files_view(request):
    context={}
    files = UserFiles.objects.filter(user=request.user)
    context['files'] = files
    return render(request,"show_files.html",context)

def delete_file_view(request,pk):
    if request.POST:
        file = UserFiles.objects.get(pk=pk)
        file.delete()
    return redirect('show_file')

@login_required(login_url='/login/')
def upload_file_view(request):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    if request.POST:
        form = FileUploadForm(request.POST,request.FILES,request=request)#, instance=request.user,request=request)
        if form.is_valid():
            print(request.user.official_name)
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            return redirect('show_file')
    else:
        form = FileUploadForm(request=request)#instance=request.user,request=request)
    context['file_form'] = form
    return render(request,"upload_file.html",context) 

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



     
@login_required(login_url='/login/')
def share_file_with_view(request,pk,pk1):
    #user_click(request)
    file = UserFiles.objects.get(pk=pk)
    user = CustomUser.objects.get(pk=pk1)
    shared_file = SharedFiles.objects.create(file=file,shared_to=user)
    shared_file.save()
    return redirect('show_file')


@login_required(login_url='/login/')
def share_file_view(request,pk):
    context = {}
    print(request.user.username)
    users = CustomUser.objects.exclude(username=request.user.username)
    context['users'] = users
    context['file_pk'] = pk
    return render(request,'share_with.html',context)



@login_required(login_url='/login/')
def show_shared_files_view(request):
    context = {}
    context['shared_files'] = SharedFiles.objects.filter(Q(shared_to=request.user)|Q(file__user=request.user)) #filter(shared_to.official_name=request.user.official_name)
    return render(request,'shared_files.html',context)

def user_click(request,pk):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    
    if request.POST:
        form = FileUploadForm(request.POST,request.FILES,request=request)#, instance=request.user,request=request)
        if form.is_valid():
            print(request.user.official_name)
            file = form.save(commit=False)
            file.user = request.user
            file.save()
            # user = CustomUser.objects.get(pk=pk)
            # shared_file = SharedFiles.objects.create(file=file,shared_to=user)
            # shared_file.save()
            #return redirect('show_file')
            if request.user.user_type=='hospital'or request.user.user_type=='professional': 
                # symp=Symptoms.objects.get(user=pk)
                print(pk)
                symptom=SymptomsShared.objects.get(pk=pk)
                print(symptom.symp.user.username)
                key = bytes(request.user.symm_key,'utf-8')
                #TODO: ADD FILE METADATA HERE
                data = b""
                #sign = hmac.new(key,bytes(data, 'utf-8'),hashlib.sha3_512)
                shared_file = SharedFiles.objects.create(file=file,shared_to=symptom.symp.user,digital_signature=sign(key,data))
                shared_file.save()
                symptom.prescription = shared_file
                print(symptom.prescription.shared_to.username)
                print("file uploaded from"+request.user.username+" for"+symptom.symp.user.username)
                #symptom.completed=True
                symptom.save()
                return render(request,"out_hosp.html")
            elif request.user.user_type=='patient':
                user = CustomUser.objects.get(pk=pk)
                if user.user_type=='pharmacy':
                    shared_file = SharedFiles.objects.create(file=file,shared_to=user)
                    shared_file.save()
                    new_request = PharmacyRequest(prescription=shared_file,from_user=CustomUser.objects.get(official_name=request.POST['shared_by']))
                    key = bytes(new_request.from_user.symm_key,'utf-8')
                    data = b""
                    '''
                    1. fetch all files from said reciever and sender
                    2. check if the new sign matches any of the existing ones
                    '''
                    files = SharedFiles.objects.filter(file__user=new_request.from_user,shared_to=request.user)
                    for file in files:
                         if verify_sign(key,data,file.digital_signature):
                              new_request.verified = True
                    # existing_sign = 
                    # new_request.verified = verify_sign()
                    new_request.save()
                    print("from2 saved")
                elif user.user_type=='insurance':
                     pass
                return render(request,"dummy2.html")
                            
            elif request.user.user_type=='patient':
                return render(request,"dummy2.html")
    else:
        form = FileUploadForm(request=request)
        context['file_form'] = form
        user = CustomUser.objects.get(pk=pk)
        if user.user_type=='pharmacy':
             user_form = SharedByForm()
             USER_CHOICES = CustomUser.objects.all().exclude(user_type="patient").exclude(user_type="pharmacy").exclude(user_type="insurance")
             user_form.fields['shared_by'].choices = [(title.official_name, title.official_name) for title in USER_CHOICES]
             context['user_form'] = user_form
        return render(request,"userclick.html",context)

      
def add_symptoms(request,pk):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    
    if request.POST:
        form = SymptomsForm(request.POST)#, instance=request.user,request=request)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()  
            print("form saved")   
            user = CustomUser.objects.get(pk=pk)
            # symp = request.POST['sympto']
            #now you can save them into related model
            temp=SymptomsShared.objects.create(symp=file,shared_to=user) 
            temp.save()
            print("temp.saved")
            return render(request,"dummy.html")
        else:
            form=SymptomsForm(instance=request.user)
            context = {'form': form}
            return render(request,'dummy.html',context)
    else:
        
        form = SymptomsForm()#instance=request.user,request=request)
        context['form'] = form
        return render(request,"symptoms.html",context)

def add_amount(request,pk):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    
    if request.POST:
        form = AmountForm(request.POST)#, instance=request.user,request=request)
        if form.is_valid():
            file = form.save(commit=False)
            file.user = request.user
            file.save()  
            print("form saved") 
            pharmacy_req = PharmacyRequest.objects.get(pk=pk)  
            user = CustomUser.objects.get(pk=pharmacy_req.prescription.file.user.pk)
            # symp = request.POST['sympto']
            #now you can save them into related model
            temp=AmountShared.objects.create(amount=file,shared_to=user) 
            temp.save()
            pharmacy_req.payment_details = temp
            pharmacy_req.save()
            print('file is',file)
            print('user is',user)

            print("temp_amount.saved")
            return render(request,"dummy.html")
        else:
            form=AmountForm(instance=request.user)
            context = {'form': form}
            return render(request,'dummy.html',context)
    
    else:
        
        form = AmountForm()#instance=request.user,request=request)
        context['form'] = form
        return render(request,"pharmacy.html",context)

def add_insurance(request,pk):
    context={}
    user = request.user
    if not user.is_authenticated: 
         return redirect('login')
    
    if request.POST:
        print('entered!!')
        form = InsuranceForm(request.POST)#, instance=request.user,request=request)
        if form.is_valid():
            print('valid_entered')
            file = form.save(commit=False)
            file.user = request.user
            file.save()  
            print("form saved")   
            user = CustomUser.objects.get(pk=pk)
            # symp = request.POST['sympto']
            #now you can save them into related model
            temp=InsuranceShared.objects.create(ins_amount=file,shared_to=user) 
            temp.save()
            print('file is',file)
            print('user is',user)

            print("InsuranceForm_amount.saved")
            return render(request,"dummy3.html")
        else:
            form=InsuranceForm(instance=request.user)
            context = {'form': form}
            return render(request,'dummy3.html',context)
    
    else:
        
        form = InsuranceForm()#instance=request.user,request=request)
        context['form'] = form
        return render(request,"insurance.html",context)
    
def symptom_valid(request,pk):
    if request.method=='POST':
            #symp=Symptoms.objects.get(user=pk)
            symptom=SymptomsShared.objects.get(pk=pk)
            print(symptom.completed)
            symptom.completed=True
            symptom.save()
                
            return redirect('hospital_index')
    else:
            # symp=Symptoms.objects.get(user=pk)
            symptom=SymptomsShared.objects.get(id=pk)
            print(symptom.completed)
            symptom.completed=True
            symptom.save()
                
            return redirect('hospital_index')
        
def amount_valid(request,pk):
    if request.method=='POST':
            symp=Amount.objects.get(user=pk)
            symptom=AmountShared.objects.get(symp=symp)
            print(symptom.completed)
            symptom.completed=1
            symptom.save()
                
            return render(request,'hospital_index.html')
    else:
            # symp=Symptoms.objects.get(user=pk)
            symptom=AmountShared.objects.get(id=pk)
            print(symptom.completed)
            symptom.completed=True
            symptom.save()
                
            return redirect('hospital_index')

def amount_pay(request):
    
    amountshared=PharmacyRequest.objects.filter(payment_details__shared_to=request.user).exclude(completed=True)
    print(amountshared)
    context={}
    
    context['amountshared']=amountshared
    # print(amount)
    # sends=[]
    # users=[]
    # for a in amountshared:
    #     print('val of a is', a)
    #     if a.shared_to == request.user:
    #         id=a.id
    #         break

    # for am in amount:
    #     # if am.id==id:
    #     print('amount is', len(am.amount)) 
    #     print(am.amount)
    #     if len(am.amount)!=0:
    #          if am.user!='ins':
    #             sends.append(am.amount)
    #             users.append(am.user)
    #          print('user to',am.user)
    #          print('user to',type(am.user))

    #     else:
    #         sends.append(1)
    #details = zip(sends, users)
     #context = {
    #         'details': details,
    #     }
   
    return render(request,'payments/pay_amount.html',context)

def insurance_pay(request):
    amount=Insurance.objects.all()
    amountshared=InsuranceShared.objects.all()
    custom_user= CustomUser.objects.all()
    print(amount)
    sends=[]
    users=[]
    try_users=[]
    for a in amountshared:
        try_users.append(a.shared_to_id)
        print('val of trial is',try_users)
        
    for i in range(len(try_users)):
         for j in range(len(custom_user)):
            if(custom_user[j].id)==try_users[i]:
             try_users[i]=custom_user[j].username

    print('try_users is',CustomUser.get_username)



    for am in amount:
        # if am.id==id:
        print('amount is', len(am.ins_amount)) 
        print(am.ins_amount)
        if len(am.ins_amount) !=0 :
            sends.append(am.ins_amount)
            users.append(am.user)
            print('user to',users)
        else:
            sends.append(100)

   
    details = zip(sends, try_users)
    ins_context = {
            'details': details,
        }
   
    return render(request,'payments/pay_insurance.html',ins_context)


    # for a in amountshared:
    #     print('shared is', a.shared_to)
    
    # print('current user is', request.user)

    # print('val of send is', send) 
    
    # return redirect(f'/payments/views/homepage?amount={send}', amount=send)