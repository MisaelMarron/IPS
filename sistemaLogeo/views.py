from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *

def permisoElevados(user):
    return user.is_staff or user.is_superuser

# Pagina de inicio 
@login_required
def index(request):
    user = request.user
    alert = False 
    if not (user.is_superuser and user.is_staff):
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

#listar usuarios, labores
@login_required
@user_passes_test(permisoElevados, login_url='/')
def listar_usuarios(request):
    usuarios = User.objects.all()
    labores = LABOR.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios,'labores': labores})

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
#modificar usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = ModificarUsuario(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = ModificarUsuario(instance=user)
    
    return render(request, 'modificar_usuario.html', {'form': form, 'user_cambio': user})
#######################################################################################################
#listar obras
@login_required
@user_passes_test(permisoElevados, login_url='/')
def listar_obras(request):
    obras = OBRA.objects.all()
    return render(request, 'obra/listar_obras.html', {'obras': obras})
#crear obra
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_obra(request):
    if request.method == 'POST':
        form = formObra(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_obras')
    else:
        form = formObra()

    return render(request, 'obra/crear_obra.html', {'form': form})
#modificar usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_obra(request, obra_CodObra):
    obra = get_object_or_404(OBRA, CodObra=obra_CodObra)
    
    if request.method == 'POST':
        form = formObra(request.POST, instance=obra)
        if form.is_valid():
            form.save()
            return redirect('listar_obras')
    else:
        form = formObra(instance=obra)
    
    return render(request, 'obra/modificar_obra.html', {'form': form, 'obra': obra})
#######################################################################################################
#listar unidades
@login_required
@user_passes_test(permisoElevados, login_url='/')
def listar_unidades(request):
    unidades = UNIDAD.objects.all()
    return render(request, 'unidades/listar_unidades.html', {'unidades': unidades})
#crear obra
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_unidad(request):
    if request.method == 'POST':
        form = formUnidad(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_unidades')
    else:
        form = formUnidad()

    return render(request, 'unidades/crear_unidad.html', {'form': form})
#modificar unidad
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_unidad(request, unidad_CodUni):
    unidad = get_object_or_404(UNIDAD, CodUni=unidad_CodUni)
    
    if request.method == 'POST':
        form = cambioUnidad(request.POST, instance=unidad)
        if form.is_valid():
            form.save()
            return redirect('listar_unidades')
    else:
        form = cambioUnidad(instance=unidad)
    
    return render(request, 'unidades/modificar_unidad.html', {'form': form, 'unidad': unidad})
#######################################################################################################
#crear labor
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_labor(request):
    if request.method == 'POST':
        form = LaborForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = LaborForm()

    return render(request, 'labor/crear_labor.html', {'form': form})
#modificar usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_labor(request, labor_CodLab):
    labor = get_object_or_404(LABOR, CodLab=labor_CodLab)
    
    if request.method == 'POST':
        form = LaborForm(request.POST, instance=labor)
        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = LaborForm(instance=labor)
    
    return render(request, 'labor/modificar_labor.html', {'form': form, 'labor': labor})


