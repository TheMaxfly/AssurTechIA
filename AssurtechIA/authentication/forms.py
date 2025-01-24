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
       fields = ['username', 'email', 'password', 'role']

   def save(self, commit=True):
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password"])  
       if commit:
           user.save()
       return user

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'last_name', 'first_name', 'role']

        
class PredictionForm(forms.ModelForm):

    age = forms.IntegerField(label='age')
    size = forms.IntegerField(label='taille')
    weight = forms.IntegerField(label='poids')
    number_children = forms.IntegerField(label='nombre d\'enfants')
    is_smoker = forms.BooleanField(label='est_il_fumeur')
    region = forms.ChoiceField(choices=Prediction.Region.choices, label='Région')



