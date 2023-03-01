from django.shortcuts import render,redirect
from .models import customer
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
import random
import time
# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    
    if request.method == "POST":
        if request.POST.get('submit') == 'sign_in':
            try:
                customerdetails=customer.objects.get(email=request.POST['email'],password=request.POST['password'])
                print(customerdetails)
                
           
            except customer.DoesNotExist as e:
                messages.info(request,'invalid credentials')
        elif request.POST.get('submit') == 'sign_up':
            name=request.POST['name']
            email=request.POST['email']
            password=request.POST['password']
            customer(name=name,email=email,password=password).save()
            send_mail(
                    subject='registered',
                    message='thanks for registering',
                    from_email = settings.EMAIL_HOST_USER,
                    recipient_list = [email,],
                    fail_silently = False,
                    
                    )
            return render(request,'login.html')
 
    return render(request,'login.html')
def forgotpassword(request):
    return render(request,'forgot.html')

def send_otp(request):
    error_message=None
    # otp=random.randint(11111,99999)
    otp=int(time.strftime('%H%S%M'))+int(time.strftime("%S"))

    email=request.POST.get('email')
    user_email=customer.objects.filter(email=email)
    if user_email:
        user=customer.objects.get(email=email)
        user.otp=otp
        user.save()
        request.session['email']=request.POST['email']
        html_message="your onetime password: - "+""+str(otp)
        subject="FORGOT PASSWORD"
        email_from = settings.EMAIL_HOST_USER
        email_to = [email]
        message = EmailMessage(subject,html_message,email_from,email_to)
        message.send()
        messages.success(request,'one time password send to your email')
        return redirect('enter_otp')

    else:
        messages.error(request,"invalid email id")
        return render(request,'forgot.html',{'error':error_message})

    # return render(request,'sentotp.html')

def enter_otp(request):
    error_message=None
    if request.session.has_key('email'):
        email=request.session['email']
        user=customer.objects.filter(email=email)
        for u in user:
            user_otp=u.otp
        if request.method =='POST':
            otp=request.POST.get('otp')
            if not otp:
                error_message='otp is required'
            elif not user_otp == otp:
                error_message='otp is invalid'

            if not error_message:
                return redirect("password_reset")
        return render(request,'enter_otp.html',{'error':error_message})
    else:
        return render(request,'forgot.html')
def password_reset(request):
    error_message=None
    if request.session.has_key('email'):
        email=request.session['email']
        user=customer.objects.get(email=email)
        
        if request.method == 'POST':
            new_password=request.POST.get('new_password')
            cnfrm_newpassword=request.POST.get('cnfrm_newpassword')
            if not new_password:
                error_message='enter new password'
            elif not cnfrm_newpassword:
                error_message='enter new confirm password'
            elif new_password == user.password:
                error_message = 'this password already exists try new password'
            if not error_message:
                user.password = new_password
                user.save()
                print(user)
                  
                messages.success(request,'password changed successfully')
                html_message="your password changed successfully"
                subject="PASSWORD CHANGED"

                email_from = settings.EMAIL_HOST_USER
                email_to = [email]
                message = EmailMessage(subject,html_message,email_from,email_to)
                message.send()
                return redirect('login')
    return render(request,'password_reset.html',{'error':error_message})