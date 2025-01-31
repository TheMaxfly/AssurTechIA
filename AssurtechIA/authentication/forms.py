# authentication/forms.py
from django import forms
from .models import User, Prediction
from django.core.exceptions import ValidationError
from django.contrib import messages


class LoginForm(forms.Form):
    email = forms.CharField(max_length=63, label="email")
    password = forms.CharField(
        max_length=63, widget=forms.PasswordInput, label="Mot de passe"
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = "customer"
        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "last_name", "first_name"]


# class PredictionForm(forms.ModelForm):

#     class Meta:
#         model = Prediction
#         fields = [
#             "genre",
#             "age",
#             "size",
#             "weight",
#             "number_children",
#             "is_smoker",
#             "region",
#         ]

def validate_positive(value):
    """Vérifie que la valeur est positive ou nulle"""
    if value < 0:
        raise ValidationError("Cette valeur doit être supérieure ou égale à 0.")

class PredictionForm(forms.ModelForm):
    age = forms.IntegerField(validators=[validate_positive], label="Âge")
    size = forms.FloatField(label="Taille (m)")
    weight = forms.FloatField(validators=[validate_positive], label="Poids (kg)")
    number_children = forms.IntegerField(validators=[validate_positive], label="Nombre d'enfants")

    class Meta:
        model = Prediction
        fields = ['genre', 'age', 'size', 'weight', 'number_children', 'is_smoker', 'region']

    def clean_size(self):
        """Validation spécifique pour s'assurer que la taille est strictement positive"""
        size = self.cleaned_data.get("size")
        if size <= 0:
            raise ValidationError("La taille doit être strictement supérieure à 0.")
        return size