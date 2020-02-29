from django.urls import path

from rango import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/<slug:category_name_slug>/add_dish/', views.add_dish, name='add_dish'),
]