from django.urls import path
from .views import LoginPageView, RegistrationPageView, LogoutView, profilView
from authentication.views import HomeView


urlpatterns = [
    
    #path('', lambda request: redirect('login')),  
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/',RegistrationPageView.as_view(), name='registration'),
    path('profil/',profilView,name='profil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("", HomeView.as_view(), name="home")

]
