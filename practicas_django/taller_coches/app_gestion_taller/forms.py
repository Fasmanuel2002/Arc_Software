from django import forms
from .models import Cliente, Coche, Servicio, CocheServicio
class ContactoForm(forms.Form):
    nombre = forms.CharField(label='Tu nombre', max_length=100)
    email = forms.EmailField(label='Tu correo electrónico')
    mensaje = forms.CharField(label='Mensaje', widget=forms.Textarea)
    
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class CocheForm(forms.ModelForm):
    class Meta:
        model = Coche
        fields = '__all__'

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = '__all__'

class CocheServicioForm(forms.ModelForm):
    class Meta:
        model = CocheServicio
        fields = '__all__'