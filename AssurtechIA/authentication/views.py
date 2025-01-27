from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, TemplateView
from .forms import RegistrationForm, LoginForm, UpdateUserForm, PredictionForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
import os
import joblib

User = get_user_model()

# Vue pour la page d'accueil
class HomeView(TemplateView):
    template_name = "authentication/home.html"

# Vue pour la déconnexion
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

# Vue pour la connexion
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
                return redirect('profil')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

# Vue pour l'inscription
class RegistrationPageView(View):
    template_name = 'authentication/inscription.html'
    form_class = RegistrationForm
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

# Vue pour le profil utilisateur
@login_required
def ProfilView(request):
    user = request.user
    return render(request, 'authentication/profil.html', {'user': user})

# Vue pour modifier le profil
@login_required
def EditProfil(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profil')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'authentication/edit_profil.html', {'form': form})

# Fonction pour calculer le BMI
def calculate_bmi(weight, height):
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)
    return bmi

# Importation correcte du transformateur personnalisé
from .custom_transformer import DropFeatureSelector

# Enregistrer le transformateur dans le contexte global
globals()['DropFeatureSelector'] = DropFeatureSelector

# Chemin du modèle
model_path = os.path.join(os.path.dirname(__file__), 'models', 'best_model.pkl')

# Fonction de chargement du modèle
def custom_load_model(model_path):
    # Charger le modèle avec le contexte global contenant DropFeatureSelector
    with open(model_path, 'rb') as f:
        model = joblib.load(f, globals())
    return model

# Chargement du modèle
model = custom_load_model(model_path)

# Vue pour les prédictions
class PredictionView(View):
    template_name = 'authentication/prediction.html'

    def get(self, request):
        form = PredictionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PredictionForm(request.POST)
        if form.is_valid():
            # Récupération des données du formulaire
            age = form.cleaned_data['age']
            weight = form.cleaned_data['weight']
            size = form.cleaned_data['size']
            number_children = form.cleaned_data['number_children']
            is_smoker = form.cleaned_data['is_smoker']
            region = form.cleaned_data['region']
            
            # Calculer le BMI
            bmi = calculate_bmi(weight, size)
            
            # Préparation des données pour la prédiction
            prediction_input = [[age, weight, size, number_children, is_smoker, region, bmi]]
            
            # Effectuer la prédiction
            try:
                prediction_result = model.predict(prediction_input)
            except Exception as e:
                return render(request, self.template_name, {'form': form, 'error': str(e)})

            # Afficher les résultats
            return render(request, self.template_name, {'form': form, 'result': prediction_result})
        
        return render(request, self.template_name, {'form': form})
