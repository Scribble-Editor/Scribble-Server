from django.contrib import admin
from django.urls import path
from .views import login, register, logout, sample_api

urlpatterns = [
  path('login', login),
  path('register', register),
  path('logout', logout),
  path('sample-api', sample_api),
]
