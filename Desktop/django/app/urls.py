from django.urls import path
from .views import *

urlpatterns=[
    path('',homepage,name='homepage'),
    path('deneme/',deneme,name='deneme'),
    path('category/<slug:slug>',category,name='category'),
    path('contact/',contact,name='contact'),
    path('delete/<slug:slug>/',delete,name='delete'),
    path('userpage/',userpage,name='userpage'),
    path('post_detail/<slug:slug>/<slug:postslug>',post_detail,name='post_detail'),
    path('dashboard/',admin_dashboard,name='admin_dashboard'),
    path('pie_chart/', pie_chart, name='pie_chart'),
    path('post_grap/<slug:slug>/',post_grap,name='post_grap'),
    path('notification/',notifications,name='notifications'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('donate/',donate,name='donate'),
    path('activate/<uidb64>/<token>/',activate,name='activate'),
    path('forgetpassword/',forgetpassword,name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',resetpassword,name='resetpassword'),
    path('success/<str:args>/', successMsg, name="success"),
    path('create/',create,name='create'),
    path('update_post/<slug:slug>/',update_post,name='update_post'),
    path('user_post_detail/<slug:slug>/',user_post_detail,name='user_post_detail'),
    path('user_post_detail/<slug:slug>/like/',like,name='like'),
    ]