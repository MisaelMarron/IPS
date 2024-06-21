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
#modificar usuario
class ModificarUsuario(forms.ModelForm):
    username = forms.CharField(max_length=30,label="Usuario")
    first_name = forms.CharField(max_length=30,label='Nombres')
    last_name = forms.CharField(max_length=30,label="Apellidos")
    email = forms.EmailField(label="Email", required=False)
    is_active = forms.BooleanField(label='Activo', required=False)
    is_staff = forms.BooleanField(label='Staff', required=False)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','is_active','is_staff']

    def clean_username(self):
        username = self.cleaned_data['username']
        user_id = self.instance.id if self.instance else None
        if User.objects.filter(username=username).exclude(id=user_id).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso. Por favor, elija otro.')
        return username
    
    def save(self, commit=True):
        user = super(ModificarUsuario, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = self.cleaned_data['is_active']
        user.is_staff = self.cleaned_data['is_staff']    

        if commit:
            user.save()

        return user 



