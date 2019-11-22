from django.contrib import admin
from django.urls import path
from .views import login, register, sample_api

urlpatterns = [
    path("compile", compileScribblet)
]