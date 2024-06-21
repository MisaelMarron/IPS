from django import forms
from django.contrib.auth.models import User

#logear usuario
class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

#crear usuario 
class agregarUsuario(forms.ModelForm):
    first_name = forms.CharField(max_length=30,label='Nombres')
    last_name = forms.CharField(max_length=30,label="Apellidos")
    email = forms.EmailField(label="Email", required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super(agregarUsuario, self).save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.cleaned_data['email']
        base_username = first_name.split()[0].lower()
        username = base_username

        numero = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{numero}"
            numero += 1

        password = f"{base_username}{last_name.split()[0].lower()}"

        # Asignar valores al usuario
        user.username = username
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        if commit:
            user.save()
        return user
 



