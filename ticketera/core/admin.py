from django.contrib import admin
from django.contrib.auth.models import User
from .models import Cliente, Ticket, Ubicacion, Evento, Comuna, Region

admin.site.register(Cliente)
admin.site.register(Ticket)
admin.site.register(Ubicacion)
admin.site.register(Evento)
admin.site.register(Comuna)
admin.site.register(Region)

