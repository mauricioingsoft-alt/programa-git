
# ==========================================================
# INVEX - PRUEBAS AUTOMÁTICAS DEL SISTEMA DE INVENTARIOS
# Evidencia SENA: GA8-220501096-AA1-EV01
# Archivo: core/test.py
# ==========================================================


# Importamos TestCase para realizar pruebas automáticas.
from django.test import TestCase

# Importamos reverse para obtener las URLs por su nombre.
from django.urls import reverse

# Importamos el modelo de usuarios de Django.
from django.contrib.auth.models import User

# Importamos nuestro modelo de productos de INVEX.
from .models import Producto


# ==========================================================
# CLASE PRINCIPAL DE PRUEBAS
# ==========================================================

# TestCase crea una base de datos temporal para las pruebas.
class PruebasInventario(TestCase):


    # ======================================================
    # PRUEBA 1 - CREACIÓN DE PRODUCTOS
    # ======================================================

    def test_crear_producto(self):

        # Creamos un usuario de prueba.
        usuario = User.objects.create_user(
            username="proveedor_prueba",
            password="ClaveSegura123!"
        )

        # Creamos un producto asociado al usuario.
        producto = Producto.objects.create(
            nombre="Arroz Diana",
            descripcion="Arroz blanco de 500 gramos",
            precio=3500,
            cantidad=100,
            proveedor=usuario
        )

        # Verificamos que se haya registrado un producto.
        self.assertEqual(
            Producto.objects.count(),
            1
        )

        # Verificamos que tenga el nombre correcto.
        self.assertEqual(
            producto.nombre,
            "Arroz Diana"
        )

        # Verificamos que la cantidad sea correcta.
        self.assertEqual(
            producto.cantidad,
            100
        )

        # Verificamos que pertenezca al usuario indicado.
        self.assertEqual(
            producto.proveedor,
            usuario
        )


    # ======================================================
    # PRUEBA 2 - PRIVACIDAD DEL INVENTARIO
    # ======================================================

    def test_inventario_privado(self):

        # Creamos el primer usuario.
        usuario1 = User.objects.create_user(
            username="andres",
            password="ClaveSegura123!"
        )

        # Creamos el segundo usuario.
        usuario2 = User.objects.create_user(
            username="carlos",
            password="ClaveSegura456!"
        )

        # Registramos un producto para Andrés.
        Producto.objects.create(
            nombre="Arroz de Andres",
            descripcion="Producto del primer proveedor",
            precio=3500,
            cantidad=100,
            proveedor=usuario1
        )

        # Registramos un producto para Carlos.
        Producto.objects.create(
            nombre="Aceite de Carlos",
            descripcion="Producto del segundo proveedor",
            precio=12000,
            cantidad=50,
            proveedor=usuario2
        )

        # Iniciamos sesión como Andrés.
        self.client.force_login(usuario1)

        # Obtenemos la URL del inventario.
        url_inventario = reverse("inventario")

        # Solicitamos la página del inventario.
        respuesta = self.client.get(url_inventario)

        # Verificamos que la página cargue correctamente.
        self.assertEqual(
            respuesta.status_code,
            200
        )

        # Comprobamos que Andrés vea su propio producto.
        self.assertContains(
            respuesta,
            "Arroz de Andres"
        )

        # Comprobamos que Andrés NO vea el producto de Carlos.
        self.assertNotContains(
            respuesta,
            "Aceite de Carlos"
        )

    # ==========================================
    # PRUEBA 3 - EDITAR UN PRODUCTO
    # ==========================================

    def test_editar_producto(self):

        # Creamos un usuario para realizar la prueba.
        usuario = User.objects.create_user(
            username="proveedor_edicion",
            password="ClaveSegura123!"
        )

        # Registramos el producto original.
        producto = Producto.objects.create(
            nombre="Arroz Diana",
            descripcion="Presentación de 500 gramos",
            precio=3500,
            cantidad=100,
            proveedor=usuario
        )

        # Iniciamos sesión con el usuario propietario.
        self.client.force_login(usuario)

        # Construimos la dirección de edición del producto.
        url = reverse(
            "editar_producto",
            args=[producto.id]
        )

        # Enviamos los nuevos valores mediante POST.
        respuesta = self.client.post(
            url,
            {
                "nombre": "Arroz Diana Premium",
                "descripcion": "Presentación de 1000 gramos",
                "precio": "4500.00",
                "cantidad": 60
            }
        )

        # Comprobamos que Django redirige al inventario.
        self.assertRedirects(
            respuesta,
            reverse("inventario")
        )

        # Recuperamos los valores actualizados de SQLite.
        producto.refresh_from_db()

        # Verificamos el cambio de nombre.
        self.assertEqual(
            producto.nombre,
            "Arroz Diana Premium"
        )

        # Verificamos el cambio de cantidad.
        self.assertEqual(
            producto.cantidad,
            60
        )

        # Verificamos el precio actualizado.
        self.assertEqual(
            producto.precio,
            4500
        )

        # Comprobamos que sigue existiendo un solo producto.
        # Así verificamos que no se creó un duplicado.
        self.assertEqual(
            Producto.objects.count(),
            1
        )

    # ==========================================
    # PRUEBA 4 - ELIMINACIÓN DE PRODUCTOS
    # ==========================================

    def test_eliminar_producto(self):

        # Creamos un usuario de prueba.
        usuario = User.objects.create_user(
            username="proveedor_eliminacion",
            password="ClaveSegura123!"
        )

        # Creamos un producto que podremos eliminar.
        producto = Producto.objects.create(
            nombre="Producto para eliminar",
            descripcion="Producto de prueba",
            precio=5000,
            cantidad=10,
            proveedor=usuario
        )

        # Iniciamos sesión como propietario.
        self.client.force_login(usuario)

        # Construimos la URL de eliminación.
        url = reverse(
            "eliminar_producto",
            args=[producto.id]
        )

        # PASO 1: Abrimos la página de confirmación.
        respuesta_get = self.client.get(url)

        # Comprobamos que la página cargue.
        self.assertEqual(
            respuesta_get.status_code,
            200
        )


        # Verificamos que aparezca el nombre del producto.
        self.assertContains(
            respuesta_get,
            producto.nombre
        )

        # Verificamos que exista el botón de confirmación.
        # Así detectaremos si la plantilla vuelve a estar vacía.
        self.assertContains(
            respuesta_get,
            "Eliminar definitivamente"
        )

        # Comprobamos que GET NO haya eliminado nada.
        self.assertEqual(
            Producto.objects.count(),
            1
        )

        # PASO 2: Confirmamos la eliminación mediante POST.
        respuesta_post = self.client.post(url)

        # Comprobamos que regrese al inventario.
        self.assertRedirects(
            respuesta_post,
            reverse("inventario")
        )

        # Comprobamos que el producto fue eliminado.
        self.assertEqual(
            Producto.objects.count(),
            0
        )


    # ==========================================
    # PRUEBA 5 - SEGURIDAD ENTRE PROVEEDORES
    # ==========================================

    def test_no_modificar_productos_ajenos(self):

        # Creamos al propietario del producto.
        propietario = User.objects.create_user(
            username="propietario",
            password="ClaveSegura123!"
        )

        # Creamos un segundo usuario sin permisos.
        intruso = User.objects.create_user(
            username="otro_usuario",
            password="ClaveSegura456!"
        )

        # Registramos un producto del propietario.
        producto = Producto.objects.create(
            nombre="Arroz protegido",
            descripcion="Producto privado",
            precio=3500,
            cantidad=100,
            proveedor=propietario
        )

        # Iniciamos sesión como el segundo usuario.
        self.client.force_login(intruso)

        # Construimos la dirección de edición.
        url_editar = reverse(
            "editar_producto",
            args=[producto.id]
        )

        # Intentamos modificar un producto ajeno.
        respuesta_editar = self.client.post(
            url_editar,
            {
                "nombre": "Producto modificado",
                "descripcion": "Cambio no autorizado",
                "precio": "100.00",
                "cantidad": 1
            }
        )

        # Django debe rechazar la operación con 404.
        self.assertEqual(
            respuesta_editar.status_code,
            404
        )

        # Recuperamos los datos originales.
        producto.refresh_from_db()

        # Comprobamos que no cambió el nombre.
        self.assertEqual(
            producto.nombre,
            "Arroz protegido"
        )

        # Comprobamos que no cambió la cantidad.
        self.assertEqual(
            producto.cantidad,
            100
        )

        # Construimos la dirección de eliminación.
        url_eliminar = reverse(
            "eliminar_producto",
            args=[producto.id]
        )

        # Intentamos eliminar el producto ajeno.
        respuesta_eliminar = self.client.post(
            url_eliminar
        )

        # Django también debe rechazar la eliminación.
        self.assertEqual(
            respuesta_eliminar.status_code,
            404
        )

        # Confirmamos que el producto sigue existiendo.
        self.assertTrue(
            Producto.objects.filter(
                id=producto.id
            ).exists()
        )
