
from django.db import models  # Importa las herramientas para definir modelos de datos.

from django.contrib.auth.models import User  # Importa el modelo de usuarios de Django.


class Producto(models.Model):  # Crea el modelo Producto, que representará una tabla.

    nombre = models.CharField(max_length=150)  # Guarda nombres de hasta 150 caracteres.

    descripcion = models.TextField(blank=True)  # Guarda una descripción opcional.

    precio = models.DecimalField(
        max_digits=12,  # Permite un máximo de 12 dígitos en total.
        decimal_places=2  # Reserva 2 posiciones para los decimales.
    )

    cantidad = models.PositiveIntegerField(default=0)  # Guarda existencias enteras no negativas.

    proveedor = models.ForeignKey(
        User,  # Asocia el producto con un usuario registrado.
        on_delete=models.CASCADE,  # Elimina sus productos si ese usuario es eliminado.
        related_name="productos"  # Permite consultar los productos asociados al usuario.
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True  # Registra cuándo se creó el producto.
    )

    def __str__(self):  # Define cómo representar el producto como texto.
        return self.nombre  # Muestra el nombre del producto.
