
from .models import Cliente, Coche, Servicio, CocheServicio
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
import json
from typing import Any
from django.shortcuts import render
from .forms import ContactoForm
from .forms import ClienteForm, CocheForm, ServicioForm, CocheServicioForm


def inicio(request):
    contexto = {'mensaje': '¡Bienvenido a mi sitio web!'}
    return render(request, 'inicio.html', contexto)


def acerca_de(request):
    return render(request, 'acerca.html', {'nombre': 'Juan Pérez'})


def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'app_gestion_taller/lista_clientes.html', {'clientes': clientes})


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



def contacto(request):
    if request.method == 'POST':
        formulario = ContactoForm(request.POST)
        if formulario.is_valid():
            # Aquí podríamos guardar o enviar los datos
            nombre = formulario.cleaned_data['nombre']
            return render(request, 'gracias.html', {'nombre': nombre})
    else:
        formulario = ContactoForm()

    return render(request, 'contacto.html', {'formulario': formulario})


def nuevo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Nuevo Cliente'})

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





@csrf_exempt
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
        return JsonResponse({"error": "Coche no encontrado"}, status=404)
       