import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Productora, Evento, Ubicacion, Ticket
from .forms import ProductoraForm, EventoForm, UbicacionForm, TicketForm, ClienteRegistroForm, ContactProdForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail


def es_admin(user):
    return user.groups.filter(name='administrador').exists()

#=========================
# PRODUCTORA
#=========================

@login_required
@user_passes_test(es_admin)
def lista_productoras(request):
    productoras = Productora.objects.all()
    return render(request, 'admin/productoras/lista.html', {'productoras': productoras})

@login_required
@user_passes_test(es_admin)
def crear_productora(request):
    form = ProductoraForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_productoras')
    return render(request, 'admin/productoras/form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def editar_productora(request, id):
    productora = get_object_or_404(Productora, id=id)
    form = ProductoraForm(request.POST or None, instance=productora)
    if form.is_valid():
        form.save()
        return redirect('lista_productoras')
    return render(request, 'admin/productoras/form.html', {'form': form})

def contacto_prod(request):
    if request.method == "POST":
        form = ContactProdForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            email = form.cleaned_data["email"]
            asunto = form.cleaned_data["asunto"]
            mensaje = form.cleaned_data["mensaje"]
            print(f"Nombre: {nombre}")
            print(f"Email: {email}")
            print(f"Asunto: {asunto}")
            print(f"Mensaje: {mensaje}")
            
            """
            send_mail(
                asunto,
                f"De: {nombre} <{email}>\n\n{mensaje}",
                email,  # remitente
                ["destinatario@ejemplo.com"],  # no importa, Mailtrap lo captura igual
            )"""


            return render(request, "contacto_prod_ok.html", {"nombre": nombre})
        
    else:
        form = ContactProdForm()
        return render(request, "contacto_prod.html", {"form": form})
    

#=========================
# UBICACIONES
#=========================

@login_required
@user_passes_test(es_admin)
def lista_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'admin/ubicaciones/lista.html', {'ubicaciones': ubicaciones})

@login_required
@user_passes_test(es_admin)
def crear_ubicacion(request):
    form = UbicacionForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('lista_ubicaciones')
    return render(request, 'admin/ubicaciones/form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def editar_ubicacion(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    form = UbicacionForm(request.POST or None, instance=ubicacion)

    if form.is_valid():
        form.save()
        return redirect('lista_ubicaciones')
    return render(request, 'admin/ubicaciones/form.html', {'form': form})

@login_required
@user_passes_test(es_admin)
def eliminar_ubicacion(request, id):
    ubicacion = get_object_or_404(Ubicacion, id=id)
    texto_confirmacion = f"¿Desea eliminar la ubicación id: #{id} ?"

    if request.method == "POST":
        ubicacion.delete()
        return redirect('lista_ubicaciones')
    return render(request, 'admin/ubicaciones/form.html', {
        'ubicacion': ubicacion,
        'texto_confirmacion': texto_confirmacion
        })

#=========================
# EVENTO
#=========================

@login_required
@user_passes_test(es_admin)
def crear_evento(request):
    form = EventoForm(request.POST or None)

    if form.is_valid():
        evento = form.save()
        return redirect('editar_tickets_evento', evento.id)
    return render(request, 'admin/eventos/form.html', {'form':form})

@login_required
@user_passes_test(es_admin)
def editar_tickets_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    form = TicketForm(request.POST or None)

    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.evento = evento
        ticket.save()
        return redirect('editar_tickets_evento', evento.id)
    
    tickets = Ticket.objects.filter(evento=evento)
    return render(request, 'admin/eventos/tickets.html', {
        'evento': evento,
        'form': form,
        'tickets': tickets
    })

def lista_eventos(request):
    eventos = Evento.objects.filter(activo=True)
    return render(request, 'eventos/lista.html', {'eventos': eventos})

def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, activo=True)
    tickets = Ticket.objects.filter(evento=evento)
    return render(request, 'eventos/detalle.html', {
        'evento': evento,
        'tickets': tickets
    })

#=========================
# CLIENTES
#=========================

def registro_cliente(request):
    form = ClienteRegistroForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        grupo = Group.objects.get(name='cliente')
        user.groups.add(grupo)
        return redirect('login')
    return render(request, 'registro.html', {'form':form})

#=========================
# CARRITO DE COMPRAS
#=========================

def agregar_carrito(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    cantidad = int(request.POST.get('cantidad', 1))

    carrito = request.session.get('carrito', {})

    if str(ticket_id) in carrito:
        carrito[str(ticket_id)]['cantidad'] += cantidad
    else:
        carrito[str(ticket_id)] = {
            'evento': ticket.evento.nombre,
            'ubicacion': ticket.ubicacion.nombre,
            'precio': int(ticket.precio),
            'cantidad': cantidad
        }
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total
    })

def eliminar_item(request, ticket_id):
    carrito = request.session.get('carrito', {})
    if str(ticket_id) in carrito:
        del carrito[str(ticket_id)]
        request.session['carrito'] = carrito
    return redirect('ver_carrito')