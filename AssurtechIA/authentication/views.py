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
from .data.functions_model import InsurancePredictor
#from selectors import DropFeatureSelector 
# from .data.functions_model import transform_bmi, bmi_calculation
import os
import joblib
import numpy
import pandas as pd
import math
import pickle

import cloudpickle 
import pickle


from django.shortcuts import render

User = get_user_model()

def custom_404(request, exception):
    return render(request, '404.html', status=404)


class HomeView(TemplateView):
    template_name = "authentication/home.html"


class AboutUsView(TemplateView):
    template_name = "authentication/about_us.html"
    

class CguView(TemplateView):
    
    template_name="authentication/cgu.html"


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
            try:
               age = form.cleaned_data['age']
               size = form.cleaned_data['size']
               weight = form.cleaned_data['weight']
               number_children = form.cleaned_data['number_children']
               is_smoker = form.cleaned_data['is_smoker']
               region = form.cleaned_data['region']
               genre = form.cleaned_data['genre']
          
           # Conversion
               genre, region, is_smoker = InsurancePredictor.convert_to_english(genre, region, is_smoker)
               print(f"Converted values: Genre={genre}, Region={region}, Smoker={is_smoker}")

           # Calcul du BMI
               if size <= 0:
                   raise ValueError("La taille doit être supérieure à zéro.")
               bmi = InsurancePredictor.bmi_calculation(weight, size)
               print(f"Calculated BMI: {bmi}")
               
            # Préparation des données pour le modèle
               input_data = pd.DataFrame({
                "age": [age],
                "sex": [genre],
                "bmi": [bmi],
                "children": [number_children],
                "smoker": [is_smoker],
                "region": [region]
                })

               model_path = os.path.join(os.path.dirname(__file__), 'data', 'best_model.pkl')
               with open(model_path, 'rb') as f:
                base_model = joblib.load(f)

               predictor = InsurancePredictor(base_model)
               pre_prediction_charge = base_model.predict(input_data)
               prediction_charge = round(pre_prediction_charge[0],2)
               print('prediction')
               print(prediction_charge)

            #    prediction = form.save(commit=False)
            #    prediction.bmi = bmi
            #    prediction.prediction_charge = prediction_charge
            #    prediction.user = request.user
            #    prediction.save()

               return redirect('profil')

            except Exception as e:
               error_message = f"Une erreur s'est produite : {str(e)}"
               print(f"Erreur : {error_message}")
               context = {
               'form': form,
               'error_message': error_message
                }
               return render(request, self.template_name, context)

       return render(request, self.template_name, {'form': form})