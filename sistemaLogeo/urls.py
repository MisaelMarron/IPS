from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('cambiar_password/', cambiar_password, name='cambiar_password'),
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
    path('modificar/<int:user_id>/', modificar_usuario, name='modificar_usuario'),
    #maquinas
    path('listar_obras/', listar_obras, name='listar_obras'),
    path('crear_obra/', crear_obra, name='crear_obra'),
    path('modificar_obra/<int:obra_CodObra>/', modificar_obra, name='modificar_obra'),


]