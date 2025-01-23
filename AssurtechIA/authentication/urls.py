from django.urls import path
from .views import LoginPageView, RegistrationPageView



urlpatterns = [
    
    #path('', lambda request: redirect('login')),  
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/',RegistrationPageView.as_view(), name='registration')
]
