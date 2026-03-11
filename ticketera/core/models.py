from django.db import models
from django.contrib.auth.models import AbstractUser

#=============================
# COMUNA REGIÓN
#=============================

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='comuna')

    def __str__(self):
        return f"{self.nombre} - {self.region.nombre}"
    
#=============================
# PRODUCTORA
#=============================

class Productora(models.Model):
    nombre = models.CharField(max_length=150)
    rut = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=200)
    giro = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre
    
class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha_evento = models.DateTimeField()
    lugar = models.CharField(max_length=150)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    productora = models.ForeignKey(Productora, on_delete=models.CASCADE, related_name="eventos")

    def __str__(self):
        return f"{self.nombre} - {self.fecha_evento.strftime('%d-%m-%Y')}"

#=============================
# VENTA DE TICKETS
#=============================

class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Ticket(models.Model):
    precio = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='tickets')
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.evento.nombre} - {self.ubicacion.nombre}"
    
class Cliente(AbstractUser):
    rut = models.CharField(max_length=10, unique=True)
    fono = models.CharField(max_length=20)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"