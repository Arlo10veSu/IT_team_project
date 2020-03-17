from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls import include
from rango import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'rango'
urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_dish/', views.add_dish, name='add_dish'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('test/', views.test, name='test'),
    path('main_course1/', views.main_course1, name='main_course1'),
    path('main_course2/', views.main_course2, name='main_course2'),
    path('main_course3/', views.main_course3, name='main_course3'),
    path('soup1/', views.soup1, name='soup1'),
    path('soup2/', views.soup2, name='soup2'),
    path('soup3/', views.soup3, name='soup3'),
    path('dessert1/', views.dessert1, name='dessert1'),
    path('dessert2/', views.dessert2, name='dessert2'),
    path('dessert3/', views.dessert3, name='dessert3'),
    path('starter1/', views.starter1, name='starter1'),
    path('starter2/', views.starter2, name='starter2'),
    path('starter3/', views.starter3, name='starter3'),
    path('remark/', views.remark, name='remark'),
    path('userInfor/', views.userInfor, name='userInfor')
]
