from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def inicio(request):
    return render(request, 'core/inicio.html')


def pagina_login(request):

    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(
            request,
            username=username,
            password=password
        )

        if usuario is not None:
            login(request, usuario)
            messages.success(request, '¡Bienvenido a INVEX!')
            return redirect('panel')

        messages.error(
            request,
            'Usuario o contraseña incorrectos.'
        )

    return render(request, 'core/login.html')


def pagina_registro(request):

    if request.user.is_authenticated:
        return redirect('panel')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not email or not password:
            messages.error(request, 'Completa todos los campos.')

        elif password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')

        elif len(password) < 8:
            messages.error(
                request,
                'La contraseña debe tener al menos 8 caracteres.'
            )

        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Ese nombre de usuario ya existe.')

        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Ese correo ya está registrado.')

        else:
            usuario = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                'Tu cuenta fue creada correctamente. Ahora puedes iniciar sesión.'
            )

            return redirect('login')

    return render(request, 'core/registro.html')


@login_required
def panel(request):
    return render(request, 'core/panel.html')


@login_required
def cerrar_sesion(request):

    if request.method == 'POST':
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')

    return redirect('inicio')
