from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='lista_eventos'),
    path('detalle_evento/<int:evento_id>', views.detalle_evento, name='detalle_evento'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('agregar_carrito/<int:ticket_id>', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar_item/<int:ticket_id>', views.eliminar_item, name='eliminar_item'),
    # ADMIN
    path('lista_productoras/', views.lista_productoras, name='lista_productoras'),
    path('crear_productora/', views.crear_productora, name='crear_productora'),
    path('editar_productora/<int:id>', views.editar_productora, name='editar_productora'),
    path('lista_ubicaciones/', views.lista_ubicaciones, name='lista_ubicaciones'),
    path('crear_ubicacion/', views.crear_ubicacion, name='crear_ubicacion'),
    path('editar_ubicacion/<int:id>', views.editar_ubicacion, name='editar_ubicacion'),
    path('eliminar_ubicacion/<int:id>', views.eliminar_ubicacion, name='eliminar_ubicacion'),
    path('crear_evento', views.crear_evento, name='crear_evento'),
    path('editar_tickets_evento/<int:evento_id>', views.editar_tickets_evento, name='editar_tickets_evento'),
]