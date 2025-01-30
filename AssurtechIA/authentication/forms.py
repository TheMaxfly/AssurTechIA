# authentication/forms.py
from django import forms
from .models import User, Prediction


class LoginForm(forms.Form):
    email = forms.CharField(max_length=63, label='email')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class RegistrationForm(forms.ModelForm):
   password = forms.CharField(widget=forms.PasswordInput, label='Mot de passe')

   class Meta:
       model = User
       fields = ['first_name', 'last_name','email', 'password']

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password"])  
       user.role = 'customer'
       if commit:
           user.save()
       return user

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'last_name', 'first_name']

        
class PredictionForm(forms.ModelForm):

    class Meta:
        model = Prediction
        fields = ['genre','age','size','weight','number_children','is_smoker','region'] 

