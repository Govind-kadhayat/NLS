
from django.contrib import admin
from django.urls import path
from NepalLicenseScholar import views

urlpatterns = [
    
    path('admin/', admin.site.urls, name='custom_admin'),  

   
    path('', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('study/', views.study, name='study'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('notice/', views.notice, name='notice'),
    path('login/', views.login_view, name='login'),
    path('api/question/', views.get_quiz, name='get_quiz'),
    path('api/submit-answers/', views.submit_answers, name='submit_answers'),
    path('main/side_bar/', views.side_bar, name='side_bar'),
    path('main/profile/', views.profile, name='profile'),
    path('main/study/', views.study, name='study'),
    path('tax/', views.tax, name='tax'),
    path('test/', views.test, name='test'),
    path('testq/', views.testq, name='testq'),
]
