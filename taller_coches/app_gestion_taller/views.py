from django.shortcuts import render
from .models import Cliente
from django.http import JsonResponse
# Create your views here.


def lista_clientes(request) -> JsonResponse:
    clientes = list(Cliente.objects.values("id", "nombre", "telefono", "email"))
    return JsonResponse(clientes, safe=False)

def detalle_cliente(request, client_id : int) -> JsonResponse:
    try:
        cliente = Cliente.objects.values("id", "nombre", "telefono", "emial").get(id=client_id)
        return JsonResponse(cliente)
    except Cliente.DoesNotExist:
        
        return JsonResponse({"error": "Cliente no encontrado"}, status=404)
