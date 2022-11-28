from django.core.mail import send_mail
import random
from .models import CustomUser, OTPMobileVerification
from django.conf import settings
import hmac
import hashlib
import os

def send_otp_email(user):
    '''
    1. generate otp using rand function
    2. store the otp in the database
    3. send the otp to the user email address
    '''

    otp = random.randint(100000,999999)
    try:
        otp_entry = OTPMobileVerification.objects.get(user=user)
        if otp_entry:
            otp_entry.otp = otp
    except Exception as e:
        otp_entry = OTPMobileVerification(user=user,otp=otp)
    otp_entry.save()

    #TODO: fill this template
    send_mail(
        "OTP verification code for email",#subject
        "OTP: "+str(otp),#message
        settings.EMAIL_HOST_USER,#from email
        [user.email,],#to email
    )
    print("email sent to"+str(user.email))

def verify_otp_email(user, otp):
    '''
    1. fetch the otp from the database for this user
    2. check if the otp duration is valid or not
    3a. if valid, compare the otp
    3b. if expired, redirect back to send otp page
    4. if otp was same, change the status of is_email_verified for the user
    '''
    otp_entry = OTPMobileVerification.objects.get(user=user)
    if otp_entry:
        #TODO: the user doesn't exist in database, so redirect to signup
        pass
    if otp == otp_entry.otp:
        #success 
        user.is_email_verified = True
        user.save()
    else:
        #TODO: raise error that otp is not correct
        pass

    pass

def sign(key,sender,reciever,path):
    size = 500 #os.path.getsize(path)
    data = bytes(sender+reciever+str(size),'utf-8')
    digest_maker = hmac.new(key,data,hashlib.sha3_512)
    return digest_maker.hexdigest()

def verify_sign(key,sender,reciever,sign,path):
    size = 500 #os.path.getsize(path)
    data = bytes(sender+reciever+str(size),'utf-8')
    digest_maker = hmac.new(key,data,hashlib.sha3_512)
    return sign == digest_maker.hexdigest()