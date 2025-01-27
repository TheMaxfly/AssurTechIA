from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, TemplateView
from .forms import RegistrationForm, LoginForm, UpdateUserForm, PredictionForm
from django.views.generic import View, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from authentication.models import Prediction, User

#from selectors import DropFeatureSelector 
from .modells.functions_model import transform_bmi, bmi_calculation
import os
import joblib

import cloudpickle 
import pickle

import math
import numpy as np
import pandas as pd

model_path = os.path.join(os.path.dirname(__file__), 'modells', 'model_pipeline_v2.pkl')
model = joblib.load(model_path)

User = get_user_model()

#model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl')
#model = joblib.load(model_path)

class HomeView(TemplateView):
    template_name = "authentication/home.html"


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('home')


class LoginPageView(View):

    template_name = 'authentication/login.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email']).first()
            if user and user.check_password(form.cleaned_data['password']):
                login(request, user)
                # redirection vers la page profil
                return redirect('profil')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})


class RegistrationPageView(View):
    template_name='authentication/inscription.html'
    form_class=RegistrationForm
    success_url = reverse_lazy('login')

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, authenticate(
                email=form.cleaned_data['email'],
                password=password,
            ))
            return redirect('home')
        return render(request, self.template_name, context={'form': form})
    
    def form_valid(self, form):
        form.save() 
        return super().form_valid(form)

@login_required
def ProfilView(request):
    user = request.user
    return render(request, 'authentication/profil.html', {'user': user})

@login_required
def EditProfil(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'authentication/edit_profil.html',{'form': form})


@login_required
def PredictionHistorical(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'authentication/prediction_historical.html', context={"predictions": predictions})


# def calculate_bmi(weight, height):
#         height_m = height / 100.0  
#         bmi = weight / (height_m ** 2)
#         return bmi

class PredictionView(View):
    template_name = 'authentication/prediction.html'

    def get(self, request):
        form = PredictionForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = PredictionForm(request.POST)
        if form.is_valid():

            genre = form.cleaned_data['genre']
            if genre == 'homme':
                genre = 'male'
            else:
                genre = 'female'

            age = int(form.cleaned_data['age'])

            weight = int(form.cleaned_data['weight'])

            size = int(form.cleaned_data['size'])

            number_children = int(form.cleaned_data['number_children'])

            is_smoker = form.cleaned_data['is_smoker']
            if is_smoker == 'oui':
                is_smoker = 'yes'
            else:
                is_smoker = 'no'
            
            region = form.cleaned_data['region']
            if region == 'sud-ouest':
                region = 'southwest'
            elif region == "nord-ouest":
                region = 'northwest'
            elif region == 'sud-est':
                region = 'southeast'
            elif region == 'nord-est':
                region = 'northeast'

            bmi = bmi_calculation(weight, size)

            input_data = pd.DataFrame({
                "age": [age],
                "sex": [genre],
                "bmi": [bmi],
                "children": [number_children],
                "smoker": [is_smoker],
                "region": [region]
            })

            pre_prediction_charge = model.predict(input_data)
            prediction_charge = round(pre_prediction_charge[0],2)
            print(prediction_charge)

            # Effectuer la prédiction
            # prediction_input = [[age, weight, size, number_children, is_smoker, region, bmi]]  
            # prediction_result = model.predict(prediction_input)

            return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form': form})



   