from django import forms
from django.contrib.auth.models import User

#logear usuario
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


 



