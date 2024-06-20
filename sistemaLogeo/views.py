from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *

# Pagina de inicio 
def index(request):
    return render(request, 'index.html')

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

