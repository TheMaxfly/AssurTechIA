from django.urls import path
from .views import LoginPageView
from django.shortcuts import redirect


urlpatterns = [
    
    path('', lambda request: redirect('login')),  
    path('login/', LoginPageView.as_view(), name='login'),
]
