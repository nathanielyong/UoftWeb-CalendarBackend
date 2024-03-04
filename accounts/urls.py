from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile')
]