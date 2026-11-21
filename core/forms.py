
# Importa las herramientas de formularios de Django.
from django import forms

# Importa el modelo de productos que ya creamos.
from .models import Producto


# Define el formulario para registrar productos.
# IMPORTANTE: este nombre debe coincidir con views.py.

class ProductoForm(forms.ModelForm):
    # Define el formulario de productos de INVEX.

    # Configura el modelo y los campos del formulario.
    class Meta:

        # Indica que el formulario utilizará el modelo Producto.
        model = Producto

        # Define los campos que podrá completar el usuario.
        fields = [
            'nombre',       # Nombre del producto.
            'descripcion',  # Información adicional del producto.
            'precio',       # Precio de venta.
            'cantidad',     # Unidades disponibles.
        ]

        # Personaliza los títulos visibles del formulario.
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción',
            'precio': 'Precio de venta',
            'cantidad': 'Unidades disponibles',
        }

    # Valida el precio antes de guardar el producto.
    def clean_precio(self):

        # Obtiene el precio después de la validación del campo.
        precio = self.cleaned_data['precio']

        # Comprueba que el precio sea mayor que cero.
        if precio <= 0:

            # Muestra un error si el precio no es válido.
            raise forms.ValidationError(
                'El precio debe ser mayor que cero.'
            )

        # Devuelve el precio cuando es válido.
        return precio
