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
    #obras
    path('listar_obras/', listar_obras, name='listar_obras'),
    path('crear_obra/', crear_obra, name='crear_obra'),
    path('modificar_obra/<int:obra_CodObra>/', modificar_obra, name='modificar_obra'),
    #unidades
    path('listar_unidades/', listar_unidades, name='listar_unidades'),
    path('crear_unidad/', crear_unidad, name='crear_unidad'),
    path('modificar_unidad/<str:unidad_CodUni>/', modificar_unidad, name='modificar_unidad'),
    #labores
    path('crear_labor/', crear_labor, name='crear_labor'),
    path('modificar_labor/<int:labor_CodLab>/', modificar_labor, name='modificar_labor'),
    #trabajadores
    path('crear_trabajo/', crear_trabajo, name='crear_trabajo'),
    path('modificar_trabajo/<int:trabajo_CodTra>/', modificar_trabajo, name='modificar_trabajo'),
    #regitro
    path('listar_registros/', listar_registros, name='listar_registros'),
    path('crear_registro/<int:trabajo_CodTra>/', crear_registro, name='crear_registro'),
    #calculo
    path('calculo_horas/', calculo_horas, name='calculo_horas'),
    path('reportes_detallados/', reportes_detallados, name='reportes_detallados'),
    path('export/pdf/', export_operarios_pdf, name='export_pdf'),
    path('export/excel/', export_operarios_excel, name='export_excel'),
    path('export/labor/pdf/', export_labor_pdf, name='export_labor_pdf'),
    path('export/labor/excel/', export_labor_excel, name='export_labor_excel'),
]