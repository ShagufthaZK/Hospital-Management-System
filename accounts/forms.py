from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from accounts.models import CustomUser, OTPMobileVerification, USER_TYPE, UserFiles, SharedFiles,Symptoms


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required, add email id")
    class Meta:
        model = CustomUser
        fields = ('email','username','password1','password2','official_name','mobile','address','user_type')

class CartForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required, add email id")
    class Meta:
        model = CustomUser
        fields = ('email','username','password1','password2','official_name','mobile','address','user_type')


class UserAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('username','password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username,password=password):
                raise forms.ValidationError("Invalid Login")

            #this code prevents users from logging in before admin has approved their accounts
            user = authenticate(username=username,password=password)
            if not user.is_approved:
                raise forms.ValidationError("Admin Approval Pending")


class ProfileEdit(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields = ('email','username','official_name','mobile','address','user_type')
        
    def clean_email(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            try:
                account=CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
            except CustomUser.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use' % email)
        
    def clean_username(self):
        if self.is_valid():
            username=self.cleaned_data['username']
            try:
                account=CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
            except CustomUser.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use' % username)


class OTPVerificationForm(forms.ModelForm):
    class Meta:
        model = OTPMobileVerification
        fields = ('otp',)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(OTPVerificationForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.is_valid():
            otp = self.cleaned_data['otp']
            try:
                user = CustomUser.objects.get(username = self.request.session.get('username') )
                otp_entry = OTPMobileVerification.objects.get(user=user)
            except Exception as e:
                raise forms.ValidationError("User does not exist") 
            if otp != otp_entry.otp:
                raise forms.ValidationError("Incorrect OTP")


class OrganizationAndHealthcareProfessionalSearchForm(forms.Form):
    name = forms.CharField(label="Name",max_length=50,required=False)
    USER_TYPE_SEARCH = USER_TYPE.copy()
    USER_TYPE_SEARCH.append(('all','All'))
    USER_TYPE_SEARCH.remove(('patient','Patient'))
    user_type = forms.ChoiceField(label="Type",choices = USER_TYPE_SEARCH,required=False)

    # class Meta:
    #     model = CustomUser
    #     fields=('official_name','user_type')
                
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ('file_name','file',)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(FileUploadForm, self).__init__(*args, **kwargs)
        
        
class SymptomsForm(forms.ModelForm):
    symp= forms.CharField(max_length=60, help_text="Enter Symptoms")
    class Meta:
        model = Symptoms
        fields = ('symp',)
    def __init__(self, *args, **kwargs):
        super(SymptomsForm, self).__init__(*args, **kwargs)
        

# class ShareFileForm(forms.Form):
#     select_user = forms.ChoiceField(label="Share with",choices = CustomUser.objects.all())
#     # class Meta:
#     #     model = SharedFiles
#     #     fields = ('shared_to',)       