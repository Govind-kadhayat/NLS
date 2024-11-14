from django.contrib import admin
from django.urls import path
from NepalLicenseScholar import views

urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Main URLs
    path('', views.login_view, name='login'),  # Corrected login function name
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('notice/', views.notice, name='notice'),

    # API URLs
    path('api/question/', views.get_quiz, name='get_quiz'),
    path('api/submit-answers/', views.submit_answers, name='submit_answers'),

    # Main App URLs
    path('main/side_bar/', views.side_bar, name='side_bar'),
    path('main/profile/', views.profile, name='profile'),
    path('main/study/', views.study, name='study'),

    # Test URLs
    path('tax/', views.tax, name='tax'),
    path('test/', views.test, name='test'),
    path('testq/', views.testq, name='testq'),
]
