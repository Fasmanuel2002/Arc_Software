
from .models import Cliente, Coche, Servicio, CocheServicio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
import json
from typing import Any

"""def lista_clientes(request) -> JsonResponse:
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)
"""


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/lista_clientes.html', {'clientes': clientes})

"""
def detalle_cliente(request, client_id : int) -> JsonResponse:
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "emial").get(id=client_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
"""

def detalle_cliente(request, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        coches = Coche.objects.filter(cliente=cliente)
        contexto = {
            'clientes': cliente,
            'coches' : coches
        }
        return render(request, 'app_gestion_taller/detalle_cliente.html', contexto)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)


@csrf_exempt
def registrar_cliente(request) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nombre=data['nombre'],
                telefono=data['telefono'],
                email=data['email']
            )
            return JsonResponse({"mensaje": "Cliente registrado con éxito", "cliente_id": cliente.id})         # type: ignore
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def registrar_coche(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.get(id=data['cliente_id'])
            coche = Coche.objects.create(
                cliente=cliente,
                marca=data['marca'],
                modelo=data['modelo'],
                matricula=data['matricula']
            )
            return JsonResponse({"mensaje": "Coche registrado con éxito", "coche_id": coche.id})
        except Cliente.DoesNotExist:
            return JsonResponse({"error": "Cliente no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)
@csrf_exempt
def registrar_servicio(request) -> JsonResponse:
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            coche = Coche.objects.get(id=data['coche_id'])
            servicio = Servicio.objects.create(nombre=data['nombre'],descripcion=data['descripcion'])
            
            CocheServicio.objects.create(coche=coche, servicio=servicio)
            return JsonResponse({"mensaje": "Servicio registrado con éxito", "servicio_id": servicio.id})
            
        except Coche.DoesNotExist:
            return JsonResponse({"error": "Coche no encontrado"}, status=404)
        except KeyError:
            return JsonResponse({"error": "Datos incompletos"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)
    
    
@csrf_exempt
def buscar_cliente(request, cliente_id : Any) -> JsonResponse:
    try:
        cliente = Cliente.objects.values('id', 'nombre', 'telefono', 'email').get(id=cliente_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
    
@csrf_exempt
def buscar_coche_por_matricula(request, matricula: Any) -> JsonResponse:
    try:
        coche = Coche.objects.select_related('cliente').get(matricula=matricula)
        
        respuesta = {
            "coche": {
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
            },
            "cliente": {
                "id": coche.cliente.id,
                "nombre": coche.cliente.nombre,
                "telefono": coche.cliente.telefono,
                "email": coche.cliente.email,
            }
        }
        return JsonResponse(respuesta)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)
            
        
@csrf_exempt
def buscar_coches_de_cliente(request, cliente_id) -> JsonResponse:
    try:
        coches = list(Coche.objects.filter(cliente_id=cliente_id).values("id", "marca", "modelo", "matricula"))
        return JsonResponse(coches, safe=False)
    
    except Cliente.DoesNotExist:
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)



def buscar_servicios_de_coche(request, coche_id):
    try:
        coche = Coche.objects.get(id=coche_id)
        coche_servicios = CocheServicio.objects.filter(coche=coche).select_related('servicio')
        contexto = {
            'coche': coche,
            'coche_servicios': coche_servicios,
        }
        return render(request, 'app_gestion_taller/servicios_coche.html', contexto)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)
        

"""@csrf_exempt
def buscar_servicios_de_coche(request, coche_id):
    try:
        coche = Coche.objects.get(id=coche_id)
        servicios = list(
            CocheServicio.objects.filter(coche=coche)
            .select_related('servicio')
            .values("servicio__id", "servicio__nombre", "servicio__descripcion")
        )
        respuesta = {
            "coche": {
                "id": coche.id,
                "marca": coche.marca,
                "modelo": coche.modelo,
                "matricula": coche.matricula,
            },
            "servicios": servicios,
        }
        return JsonResponse(respuesta)
    except Coche.DoesNotExist:
        return JsonResponse({"error": "Coche no encontrado"}, status=404)"""
        
        