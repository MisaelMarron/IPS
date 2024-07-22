from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from .models import *

def permisoElevados(user):
    return user.is_staff or user.is_superuser

# Pagina de inicio 
@login_required
def index(request):
    user = request.user   
    alert = False 
    labores_usuario = LABOR.objects.filter(CodUsu=user)
    trabajos_asignados = TRABAJO.objects.filter(CodLab__in=labores_usuario)

    if user.is_superuser and user.is_staff:
        trabajos = TRABAJO.objects.all()
        return render(request, 'panelAdmin.html', {'alerta': alert,'trabajos': trabajos,'trabajos_asignados':trabajos_asignados})
    else:
        alert = True
        return render(request, 'panelUser.html', {'alerta': alert,'trabajos_asignados':trabajos_asignados})
        

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
                messages.success(request, 'Se inicio correctamente la sesion')
                return redirect('index') 
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#cerrar seccion 
@login_required
def logout_views(request):
    logout(request)
    messages.success(request, 'Se cerro correctamente la sesion')
    return redirect('login')

#Cambiar contraseñas
@login_required
def cambiar_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.success(request, 'Se cambio la contraseña correctamente')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'cambiar_password.html', {'form': form})

#listar usuarios, labores, trabajos
@login_required
@user_passes_test(permisoElevados, login_url='/')
def listar_usuarios(request):
    usuarios = User.objects.all()
    labores = LABOR.objects.all()
    trabajos = TRABAJO.objects.all()
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios,'labores': labores,'trabajos': trabajos})

#crear usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_usuario(request):
    if request.method == 'POST':
        form = agregarUsuario(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            messages.success(request, f'Se creó un nuevo usuario "{user.username}"')
            messages.success(request, f'Con contraseña "{user.first_name.split()[0].lower()}{user.last_name.split()[0].lower()}"')
            return redirect('listar_usuarios')
    else:
        form = agregarUsuario()

    return render(request, 'crear_usuario.html', {'form': form})
#modificar usuarios
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_usuario(request, user_id):
    user = get_object_or_404(User, id=user_id)  
    mismo = user_id == request.user.id
    if request.method == 'POST':
        form = ModificarUsuario(request.POST, instance=user)
        if form.is_valid():
            if (form.instance.is_active and form.instance.is_superuser) or (form.instance.id != request.user.id):
                messages.success(request, f'Modifico correctamente "{form.instance.username}"')
                form.save()
            else:
                messages.warning(request, 'No se puede desactivar/ni quitar administrador a usted mismo')
            return redirect('listar_usuarios')
    else:
        form = ModificarUsuario(instance=user)
    
    return render(request, 'modificar_usuario.html', {'form': form, 'user_cambio': user, 'mismo':mismo})
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
            messages.success(request, 'Se agrego una nueva obra')
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
            messages.success(request, 'Se modifico correctamente')
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
            messages.success(request, 'Se agrego un nueva unidad')
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
            messages.success(request, 'Se modifico correctamente')
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
            messages.success(request, 'Se inscribio en nueva labor')
            form.save()
            return redirect('listar_usuarios')
    else:
        form = LaborForm()

    return render(request, 'labor/crear_labor.html', {'form': form})
#modificar labor
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_labor(request, labor_CodLab):
    labor = get_object_or_404(LABOR, CodLab=labor_CodLab)
    
    if request.method == 'POST':
        form = LaborForm(request.POST, instance=labor)
        if form.is_valid():
            messages.success(request, 'Se modifico correctamente')
            form.save()
            return redirect('listar_usuarios')
    else:
        form = LaborForm(instance=labor)
    
    return render(request, 'labor/modificar_labor.html', {'form': form, 'labor': labor})
#######################################################################################################
#crear trabajo
@login_required
@user_passes_test(permisoElevados, login_url='/')
def crear_trabajo(request):
    if request.method == 'POST':
        form = TrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se agrego correctamente')
            return redirect('listar_usuarios')
    else:
        form = TrabajoForm()

    return render(request, 'trabajo/crear_trabajo.html', {'form': form})
#modificar trabajo
@login_required
@user_passes_test(permisoElevados, login_url='/')
def modificar_trabajo(request, trabajo_CodTra):
    trabajo = get_object_or_404(TRABAJO, CodTra=trabajo_CodTra)
    
    if request.method == 'POST':
        form = TrabajoForm(request.POST, instance=trabajo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se modifico correctamente')
            return redirect('listar_usuarios')
    else:
        form = TrabajoForm(instance=trabajo)
    
    return render(request, 'trabajo/modificar_trabajo.html', {'form': form, 'trabajo': trabajo})
#######################################################################################################
# listar registro
@login_required
def listar_registros(request):
    user = request.user   
    labores_usuario = LABOR.objects.filter(CodUsu=user)
    trabajos_asignados = TRABAJO.objects.filter(CodLab__in=labores_usuario)
    registros_asignados = REGISTRO.objects.filter(CodTra__in=trabajos_asignados).order_by('FecTra')
    return render(request, 'registro/listar_registros.html', {'registros_asignados':registros_asignados})
# crear registro
@login_required
def crear_registro(request, trabajo_CodTra):
    user = request.user
    
    # Obtener el trabajo si existe y pertenece al usuario
    trabajo = get_object_or_404(TRABAJO, CodTra=trabajo_CodTra, CodLab__CodUsu=user)
    maquina = trabajo.CodLab.CodUni.NomUni
    if request.method == 'POST' and trabajo.CodLab.CodUsu.username == user.username:
        form = RegistroForm(request.POST)
        form.instance.CodTra = trabajo 
        form.instance.HorIni = trabajo.CodLab.CodUni.HorUni
        if form.is_valid():
            trabajo.CodLab.CodUni.HorUni = form.instance.HorFin
            form.save()
            unidad = get_object_or_404(UNIDAD, CodUni=trabajo.CodLab.CodUni.CodUni)
            unidad.HorUni = form.instance.HorFin
            unidad.save()
            messages.success(request, 'Se agrego correctamente')
            return redirect('listar_registros') 
    else:
        form = RegistroForm()

    return render(request, 'registro/crear_registro.html', {'form': form,"maquina":maquina})
#######################################################################################################
#calcular automatizado de horas trabajados
@login_required
@user_passes_test(permisoElevados, login_url='/')
def calculo_horas(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario', 'nada')
        if id_usuario != "nada":
            user = get_object_or_404(User, id=id_usuario)
            labores_usuario = LABOR.objects.filter(CodUsu=user)
            trabajos_asignados = TRABAJO.objects.filter(CodLab__in=labores_usuario)
            registros_asignados = REGISTRO.objects.filter(CodTra__in=trabajos_asignados).order_by('FecTra')
            total = 0
            for registro in registros_asignados:
                registro.horas_totales = registro.HorFin - registro.HorIni
                total += registro.horas_totales
            return render(request, 'herramientas/calculo_horas_usuario.html',{'registros':registros_asignados,'total':total,'usuario':user})
            
    return render(request, 'herramientas/calculo_horas.html',{'usuarios':usuarios})

#generar reporte detallados 
#Reporte de maquina de tiempo a tiempo
#liquidacion a trabajador por todo el tiempo
def reportes_detallados(request):
    obras = OBRA.objects.all()
    contratistas = obras.values_list('NomCon', flat=True).distinct()
    print(contratistas)
    return render(request, 'reportes/listar_reportes.html', {'obras': obras, 'contratistas': contratistas})

def unidades_por_obra(_, obra_CodObra):
    obra = get_object_or_404(OBRA, CodObra=obra_CodObra)
    unidades = UNIDAD.objects.filter(labores__trabajo__CodObra=obra).distinct()
    data = [{'id': unidad.CodUni, 'nombre': unidad.NomUni} for unidad in unidades]
    return JsonResponse(data, safe=False)
