# authentication/urls.py
from django.urls import path
from .views import LoginPageView, RegistrationPageView, LogoutView, ProfilView, EditProfil, PredictionHistorical, HomeView, PredictionView,AboutUsView
#from . import views

urlpatterns = [
    path('login/', LoginPageView.as_view(), name='login'),
    path('registration/', RegistrationPageView.as_view(), name='registration'),
    path('profil/', ProfilView, name='profil'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', HomeView.as_view(), name='home'),
    path('profil/edit/', EditProfil, name='edit_profil'),
    #path('prediction/', PredictionView.as_view(), name='prediction'),
    path('historical/', PredictionHistorical, name='historical'),
    path('aboutus/',AboutUsView.as_view(),name='aboutus'),
    #path('cgu/',CguView.as_view,name='cgu'),
]   

