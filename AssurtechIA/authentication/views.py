from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View, TemplateView
from .forms import RegistrationForm, LoginForm, UpdateUserForm
from django.views.generic import View, ListView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


User = get_user_model()


Modele = 


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


class historique(ListView):



class PredictionView(View):



   