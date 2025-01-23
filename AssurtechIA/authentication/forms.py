# authentication/forms.py
from django import forms
from .models import User

class LoginForm(forms.Form):
    email = forms.CharField(max_length=63, label='email')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')



class RegistrationForm(forms.ModelForm):
   password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

   class Meta:
       model = User
       fields = ['username', 'email', 'password', 'role']

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password"])  
       if commit:
           user.save()
       return user