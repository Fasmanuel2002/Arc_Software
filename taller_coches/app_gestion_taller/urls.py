from django.urls import path
from .views import lista_clientes, detalle_cliente
from .views import (
    registrar_cliente, registrar_coche, registrar_servicio,
    buscar_cliente, buscar_coche_por_matricula,
    buscar_coches_de_cliente, buscar_servicios_de_coche
)

urlpatterns = [
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/<int:cliente_id>/', detalle_cliente, name='detalle_cliente'),
    path('clientes/registrar/', registrar_cliente, name='registrar_cliente'),
    path('coches/regisrar/', registrar_coche, name='registrar_coche'),
    path('servicios/registrar/', registrar_servicio, name='registrar_servicio'),
    path('clientes/<int:cliente_id>/', buscar_cliente, name='buscar_cliente'),
    path('coches/matricula/<str:matricula>/', buscar_coche_por_matricula, name='buscar_coche_por_matricula'),
    path('clientes/<int:cliente_id>/coches/', buscar_coches_de_cliente, name='buscar_coches_de_cliente'),
    path('coches/<int:coche_id>/servicios/', buscar_servicios_de_coche, name='buscar_servicios_de_coche'),
]