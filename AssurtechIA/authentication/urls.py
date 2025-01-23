from django.urls import path
from .views import LoginPageView, HomeView


urlpatterns = [
    
    path("login/", LoginPageView.as_view(), name="login"),
    path("", HomeView.as_view(), name="home")
]
