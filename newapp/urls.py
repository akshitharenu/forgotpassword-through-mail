from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('forgot',views.forgotpassword,name='forgotpassword'),
    path('sentotp',views.send_otp,name='sent_otp'),
    path('enter_otp',views.enter_otp,name='enter_otp'),
    path('password_reset/',views.password_reset,name='password_reset')


]