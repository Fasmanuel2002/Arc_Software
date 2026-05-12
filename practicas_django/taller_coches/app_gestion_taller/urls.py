from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('clientes/registrar/', views.registrar_cliente, name='registrar_cliente'),
    path('coches/registrar/', views.registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', views.registrar_servicio, name='registrar_servicio'),
    path('clientes/<int:cliente_id>/', views.buscar_cliente, name='buscar_cliente'),
    path('coches/matricula/<str:matricula>/', views.buscar_coche_por_matricula, name='buscar_coche_por_matricula'),
    path('clientes/<int:cliente_id>/coches/', views.buscar_coches_de_cliente, name='buscar_coches_de_cliente'),
    path('coches/<int:coche_id>/servicios/', views.buscar_servicios_de_coche, name='buscar_servicios_de_coche'),

    path('', views.inicio, name='inicio'),
    path('acerca/', views.acerca_de, name='acerca'),
     path('contacto/', views.contacto, name='contacto'),
     path('clientes/nuevo/', views.nuevo_cliente, name='nuevo_cliente')

]