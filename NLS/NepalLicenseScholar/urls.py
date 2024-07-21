from django.contrib import admin
from django.urls import path,include
from NepalLicenseScholar import views

urlpatterns = [
    path ("home", views.home, name='home'),
      path ("about", views.about, name='about'),
      path ("contact", views.contact, name='contact'),
    path ("", views.dashboard, name='dashbaord'),
]
