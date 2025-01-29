"""
URL configuration for AssurtechIA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# AssurtechIA/urls.py
from django.conf.urls import handler404
from django.contrib import admin
from django.urls import path, include
from authentication.views import HomeView, CguView,AboutUsView,PredictionView,prediction_result
#import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", HomeView.as_view(), name="home"),
    path('cgu/',CguView.as_view(),name='cgu'),
    path('aboutus/',AboutUsView.as_view(),name='aboutus'),
    #path('aboutus/',AboutUsView.as_view(),name='aboutus'),
    path('prediction/', PredictionView.as_view(), name='prediction'),
    path('prediction/result/', prediction_result, name='result'),
    #path('cgu/',CguView, name="cgu"),
    # Ajoutez d'autres URLs ici
]

handler404 = 'authentication.views.custom_404'
