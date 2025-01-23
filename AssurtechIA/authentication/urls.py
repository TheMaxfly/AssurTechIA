from django.urls import path
from .views import LoginPageView, RegistrationPageView,profilView
from authentication.views import HomeView


urlpatterns = [
    
    #path('', lambda request: redirect('login')),  
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/',RegistrationPageView.as_view(), name='registration'),
    path('profil/',profilView,name='profil'),
    path("", HomeView.as_view(), name="home")
]
