from django.contrib import admin

from .models import Producto #Importa nuestro modelo producto desde model.py
# Registra el modelo Producto en el administrador
@admin.register(Producto)
class productoAdmin (admin.ModelAdmin): #Configura como se muestran los productos

    list_display =(
        'nombre',          # Muestra el nombre del producto.
        'precio',          # Muestra el precio registrado.
        'cantidad',        # Muestra las unidades disponibles.
        'proveedor',       # Muestra el usuario asociado.
        'fecha_creacion',  # Muestra cuándo se creó.
    )

search_fields = ("nombre",) #Permite buscar productos poe su nombre
list_filter = ('fecha_creacion',)  # Permite filtrar por fecha de creación.
