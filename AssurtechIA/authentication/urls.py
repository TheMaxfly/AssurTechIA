# authentication/urls.py
from django.urls import path
from .views import LoginPageView, RegistrationPageView, LogoutView, ProfilView, EditProfil, PredictionHistorical, PredictionView, HomeView, CguView

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/', RegistrationPageView.as_view(), name='registration'),
    path('profil/', ProfilView, name='profil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('', HomeView.as_view(), name='home'),
    path('profil/edit/', EditProfil, name='edit_profil'),
    path('historical/', PredictionHistorical, name='historical'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
    # path('cgu/', CguView.as_view(), name='cgu'),
]

