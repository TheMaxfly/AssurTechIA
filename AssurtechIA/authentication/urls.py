from django.urls import path
from .views import LoginPageView, profilView


urlpatterns = [
    
    path("login/", LoginPageView.as_view(), name="login"),
    path("profil/", profilView, name="profil")
]
