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
from accounts.views import * #editprofile, registration_view, logout_view, login_view, patient_view, editprofile, hospital_view, insurance_view, pharmacy_view, healthcare_prof_view, otp_email_view, upload_file_view, show_files_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('share_file/<int:pk>',share_file_view, name="share_file"),
    path('share_with/<int:pk>/<int:pk1>',share_file_with_view, name="share_file_with"),
    path('show_shared_file/',show_shared_files_view, name="show_shared_file"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)