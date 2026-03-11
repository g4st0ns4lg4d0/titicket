from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Productora, Evento, Ubicacion, Ticket, Cliente

class ProductoraForm(forms.ModelForm):
    class Meta:
        model = Productora
        fields = "__all__"

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = "__all__"

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = "__all__"

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['ubicacion','precio','stock']

class ClienteRegistroForm(UserCreationForm):
    class Meta:
        model = Cliente
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'rut',
            'fono',
            'comuna',
            'password1',
            'password2'
        ]
class ContactProdForm(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    email = forms.EmailField(label="Correo Electrónico")
    asunto = forms.CharField(max_length=150, label="Asunto")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
