from django.views.generic.detail import DetailView

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.generic import View # import des fonctions login et authenticate
from . import forms
from django.contrib.auth.decorators import login_required

class LoginPageView(View):
    template_name = 'authentication/login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        message = ''
        return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                # redirection vers la page profil
                return redirect('profil')
        message = 'Identifiants invalides.'
        return render(request, self.template_name, context={'form': form, 'message': message})

@login_required
def profilView(request):
    user = request.user
    return render(request, 'authentication/profil.html', {'user': user})
    
