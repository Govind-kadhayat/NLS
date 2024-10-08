from django.contrib import admin
from django.urls import path,include
from NepalLicenseScholar import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('dashboard', views.dashboard, name='dashboard'),
    path ("", views.dashboard, name='dashbaord'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('notice', views.notice, name='notice'),
    path('api/question/', views.get_quiz, name='get_quiz'),  
    path('main/side_bar', views.side_bar, name='side_bar'),
    path('main/profile', views.profile, name='profile'),
    path('main/study', views.study, name='study'),
    path('tax', views.tax, name='tax'),
    path('test', views.test, name='test'),
    path('testq/', views.testq, name='testq'),
    path('api/submit-answers/', views.submit_answers, name='submit_answers'),

]