from django.contrib import admin
from .models import Cliente, Coche, Servicio, CocheServicio
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Coche)
admin.site.register(Servicio)
admin.site.register(CocheServicio)
