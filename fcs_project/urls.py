"""fcs_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from accounts.views import *
# editprofile, registration_view, logout_view, login_view, patient_view, editprofile, cart,add_to_cart
from payments.views import *
# from payments.views import paymenthandler,homepage
# from medicines.views import CreateCheckoutSessionView,ProductLandingPageView
from accounts.views import * #editprofile, registration_view, logout_view, login_view, patient_view, editprofile, hospital_view, insurance_view, pharmacy_view, healthcare_prof_view, otp_email_view, upload_file_view, show_files_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/views/homepage',homepage, name='payments'),
    path('pay/',amount_pay, name="cart_name"),
    path('ins_pending/',insurance_pay, name="ins_pay"),

    path('payments/views/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('signup/',registration_view, name="signup"),
    path('otp_email/',otp_email_view, name="otp_email"),
    path('logout/',logout_view, name="logout"),
    path('login/',login_view, name="login"),
    path('edit/', editprofile, name="edit"),
    path('patient_index/', patient_view, name="patient_index"),#this also has the catalogue search
    path('hospital_index/', hospital_view, name="hospital_index"),
    path('insurance_index/', insurance_view, name="insurance_index"),
    path('pharmacy_index/', pharmacy_view, name="pharmacy_index"),
    path('health_prof_index/', healthcare_prof_view, name="health_prof_index"),
    path('edit/',editprofile, name="edit"),
    path('upload_file/',upload_file_view, name="upload_file"),
    path('show_file/',show_files_view, name="show_file"),
    path('show_file/<int:pk>',delete_file_view, name="delete_file"),
    path('payments/views/claim_refund/',claim, name="refund_name"),
    path('payments/views/get_insurance', get_insurance, name="get_insurance"),
    path('payments/views/insurance_claimed', insurance_claimed, name="insurance_claimed"),
    # path('', homepage, name='index'),
    path('share_file/<int:pk>',share_file_view, name="share_file"),
    path('share_with/<int:pk>/<int:pk1>',share_file_with_view, name="share_file_with"),
    path('show_shared_file/',show_shared_files_view, name="show_shared_file"),
    path('userclick/<int:pk>',user_click, name="userclick"),
    path('symptoms/<int:pk>',add_symptoms, name="symptoms"),
    path('amount/<int:pk>',add_amount, name="amount"),
    path('insurance/<int:pk>',add_insurance, name="insurance"),


    path('hospital_index/<int:pk>',symptom_valid, name="symptom_valid"),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),
    
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_complete.html'),
     name='password_reset_complete'),
   
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)