
# ==================================================
# INVEX - SISTEMA DE GESTIÓN DE INVENTARIOS
# ARCHIVO: core/views.py
# EVIDENCIA: GA8-220501096-AA1-EV01
# ==================================================


# ==================================================
# IMPORTACIONES
# ==================================================

# Permite mostrar páginas, redirigir y buscar objetos.
from django.shortcuts import render, redirect, get_object_or_404

# Funciones del sistema de autenticación de Django.
from django.contrib.auth import authenticate, login, logout

# Protege las vistas que requieren inicio de sesión.
from django.contrib.auth.decorators import login_required

# Modelo de usuarios incluido en Django.
from django.contrib.auth.models import User

# Permite mostrar mensajes de éxito o error.
from django.contrib import messages

# Importa nuestro modelo de productos.
from .models import Producto

# Importa el formulario para registrar y editar productos.
from .forms import ProductoForm


# ==================================================
# 1. PÁGINA PRINCIPAL
# ==================================================

def inicio(request):

    # Muestra la página principal de INVEX.
    return render(
        request,
        'core/inicio.html'
    )


# ==================================================
# 2. INICIAR SESIÓN
# ==================================================

def pagina_login(request):

    # Si ya inició sesión, lo enviamos al panel.
    if request.user.is_authenticated:
        return redirect('panel')

    # Comprueba si el usuario envió sus credenciales.
    if request.method == 'POST':

        # Obtiene los valores del formulario HTML.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Comprueba si las credenciales son correctas.
        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        # Si Django encontró un usuario válido.
        if usuario is not None:

            # Inicia la sesión.
            login(request, usuario)

            # Prepara un mensaje de bienvenida.
            messages.success(
                request,
                '¡Bienvenido a INVEX!'
            )

            # Redirige al panel privado.
            return redirect('panel')

        # Muestra un error cuando las credenciales fallan.
        messages.error(
            request,
            'Usuario o contraseña incorrectos.'
        )

    # Muestra la página de inicio de sesión.
    return render(
        request,
        'core/login.html'
    )


# ==================================================
# 3. REGISTRAR USUARIOS
# ==================================================

def pagina_registro(request):

    # Un usuario autenticado no necesita registrarse otra vez.
    if request.user.is_authenticated:
        return redirect('panel')

    # Comprueba si se envió el formulario de registro.
    if request.method == 'POST':

        # Obtiene el nombre de usuario y elimina espacios externos.
        username = request.POST.get('username', '').strip()

        # Obtiene el correo electrónico.
        email = request.POST.get('email', '').strip()

        # Obtiene la contraseña.
        password = request.POST.get('password')

        # Obtiene la confirmación de contraseña.
        password2 = request.POST.get('password2')

        # Comprueba los campos obligatorios.
        if not username or not email or not password:

            messages.error(
                request,
                'Completa todos los campos.'
            )

        # Verifica que ambas contraseñas sean iguales.
        elif password != password2:

            messages.error(
                request,
                'Las contraseñas no coinciden.'
            )

        # Verifica la longitud mínima.
        elif len(password) < 8:

            messages.error(
                request,
                'La contraseña debe tener al menos 8 caracteres.'
            )

        # Evita registrar nombres de usuario repetidos.
        elif User.objects.filter(username=username).exists():

            messages.error(
                request,
                'Ese nombre de usuario ya existe.'
            )

        # Evita registrar correos repetidos.
        elif User.objects.filter(email=email).exists():

            messages.error(
                request,
                'Ese correo ya está registrado.'
            )

        else:

            # Crea el usuario utilizando el sistema de Django.
            # Django almacena un hash de la contraseña.
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Informa que la cuenta fue creada.
            messages.success(
                request,
                'Tu cuenta fue creada correctamente. '
                'Ahora puedes iniciar sesión.'
            )

            # Envía al formulario de inicio de sesión.
            return redirect('login')

    # Muestra el formulario de registro.
    return render(
        request,
        'core/registro.html'
    )


# ==================================================
# 4. PANEL PRINCIPAL
# ==================================================

# Solo permite el acceso a usuarios autenticados.
@login_required
def panel(request):

    # Muestra el panel de INVEX.
    return render(
        request,
        'core/panel.html'
    )


# ==================================================
# 5. CERRAR SESIÓN
# ==================================================

# Protege el cierre de sesión.
@login_required
def cerrar_sesion(request):

    # Solo cierra sesión si la solicitud es POST.
    if request.method == 'POST':

        # Finaliza la sesión actual.
        logout(request)

        # Prepara un mensaje informativo.
        messages.success(
            request,
            'Has cerrado sesión correctamente.'
        )

    # Regresa a la página principal.
    return redirect('inicio')


# ==================================================
# 6. CONSULTAR INVENTARIO
# ==================================================

# Solo los usuarios autenticados pueden ver su inventario.
@login_required
def inventario(request):

    # Obtiene los productos del proveedor autenticado.
    # No muestra productos de otros proveedores.
    productos = Producto.objects.filter(
        proveedor=request.user
    ).order_by('nombre')

    # Prepara la información para la plantilla HTML.
    contexto = {
        'productos': productos
    }

    # Muestra la tabla de inventarios.
    return render(
        request,
        'core/inventario.html',
        contexto
    )


# ==================================================
# 7. REGISTRAR NUEVO PRODUCTO
# ==================================================

# Impide registrar productos sin iniciar sesión.
@login_required
def nuevo_producto(request):

    # Comprueba si el usuario envió el formulario.
    if request.method == 'POST':

        # Construye el formulario con la información recibida.
        form = ProductoForm(request.POST)

        # Ejecuta las validaciones definidas en forms.py.
        if form.is_valid():

            # Prepara el producto sin guardarlo todavía.
            producto = form.save(commit=False)

            # Asigna como proveedor al usuario autenticado.
            producto.proveedor = request.user

            # Guarda el producto en SQLite.
            producto.save()

            # Prepara el mensaje de éxito.
            messages.success(
                request,
                '¡Producto registrado correctamente!'
            )

            # Regresa al inventario.
            return redirect('inventario')

    else:

        # Si es GET, crea un formulario vacío.
        form = ProductoForm()

    # Envía el formulario al HTML.
    # Si hay errores, conserva los datos ingresados.
    contexto = {
        'form': form
    }

    # Muestra la página de registro.
    return render(
        request,
        'core/nuevo_producto.html',
        contexto
    )


# ==================================================
# 8. EDITAR PRODUCTO
# ==================================================

# Solo permite editar productos a usuarios autenticados.
@login_required
def editar_producto(request, producto_id):

    # Busca el producto por su ID y verifica su propietario.
    # Si el producto no existe o pertenece a otro usuario,
    # Django devuelve un error 404.
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        proveedor=request.user
    )

    # Comprueba si se enviaron cambios al formulario.
    if request.method == 'POST':

        # Carga los nuevos datos sobre el producto existente.
        # instance=producto evita crear un producto duplicado.
        form = ProductoForm(
            request.POST,
            instance=producto
        )

        # Comprueba que los nuevos datos sean válidos.
        if form.is_valid():

            # Actualiza el registro original en SQLite.
            form.save()

            # Prepara un mensaje de confirmación.
            messages.success(
                request,
                '¡Producto actualizado correctamente!'
            )

            # Regresa al inventario.
            return redirect('inventario')

    else:

        # Si el usuario abre la página mediante GET,
        # carga los datos actuales del producto.
        form = ProductoForm(
            instance=producto
        )

    # Prepara la información para el HTML.
    contexto = {
        'form': form,
        'producto': producto
    }

    # Muestra el formulario de edición.
    return render(
        request,
        'core/editar_producto.html',
        contexto
    )


# ==================================================
# 9. ELIMINAR PRODUCTO
# ==================================================

# Solo permite eliminar productos a usuarios autenticados.
@login_required
def eliminar_producto(request, producto_id):

    # Busca el producto por su identificador.
    # También comprueba que pertenezca al usuario actual.
    # Esto impide eliminar productos de otros proveedores.
    producto = get_object_or_404(
        Producto,
        id=producto_id,
        proveedor=request.user
    )

    # Comprueba si el usuario confirmó la eliminación.
    if request.method == 'POST':

        # Elimina definitivamente el producto de SQLite.
        producto.delete()

        # Prepara un mensaje de confirmación.
        messages.success(
            request,
            '¡Producto eliminado correctamente!'
        )

        # Después de eliminar, regresa al inventario.
        return redirect('inventario')

    # Si el usuario abre la dirección mediante GET,
    # NO se elimina nada.
    # Únicamente se muestra la página de confirmación.
    contexto = {
        'producto': producto
    }

    # Muestra el formulario de confirmación.
    return render(
        request,
        'core/eliminar_producto.html',
        contexto
    )
