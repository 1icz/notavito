from django.urls import path
from . import views

urlpatterns = [
    path('', views.account, name='account'),
    path('edit/', views.edit_profile, name='edit_profile'),
]