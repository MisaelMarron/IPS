from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .forms import *

def permisoElevados(user):
    return user.is_staff or user.is_superuser

# Pagina de inicio 
@login_required
def index(request):
    user = request.user
    alert = False  # Inicializar alert en False por defecto

    if user.is_authenticated:
        first_name = user.first_name.strip().split()[0].lower() if user.first_name else ''
        last_name = user.last_name.strip().split()[0].lower() if user.last_name else ''

        if first_name and last_name:
            password_to_check = f"{first_name}{last_name}"
            if user.check_password(password_to_check):
                alert = True

    return render(request, 'index.html', {'alerta': alert})

#iniciar seccion
def login_views(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index') 
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#cerrar seccion 
@login_required
def logout_views(request):
    logout(request)
    return redirect('login')

#Cambiar contraseñas
@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'cambiar_password.html', {'form': form})

#listar usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})

#crear usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_usuario(request):
    if request.method == 'POST':
        form = agregarUsuario(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = agregarUsuario()

    return render(request, 'crear_usuario.html', {'form': form})