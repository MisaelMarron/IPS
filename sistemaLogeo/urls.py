from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login/', login_views, name='login'),
    path('logout/', logout_views, name='logout'),
    path('cambiar_password/', cambiar_password, name='cambiar_password'),
    path('listar_usuarios/', listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', crear_usuario, name='crear_usuario'),
]