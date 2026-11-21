
# Importa la herramienta para definir rutas.
from django.urls import path

# Importa las funciones que tenemos en views.py.
from . import views


# Lista de direcciones disponibles en INVEX.
urlpatterns = [

    # Página principal del sistema.
    path('', views.inicio, name='inicio'),

    # Formulario para iniciar sesión.
    path('login/', views.pagina_login, name='login'),

    # Formulario para registrar usuarios.
    path('registro/', views.pagina_registro, name='registro'),

    # Panel principal del usuario autenticado.
    path('panel/', views.panel, name='panel'),

    # Permite cerrar la sesión.
    path(
        'cerrar-sesion/',
        views.cerrar_sesion,
        name='cerrar_sesion'
    ),

    # Muestra los productos registrados por el usuario
    path(
        'inventario/',
        views.inventario,
        name='inventario'
    ),

    # Muestra el formulario para crear productos
    path(
        'nuevo-producto/',
        views.nuevo_producto,
        name='nuevo_producto'
    ),

    # NUEVA RUTA: permite editar productos existentes
    path(
        'editar-producto/<int:producto_id>/', views.editar_producto, name='editar_producto'
    ),

    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'
),

]
