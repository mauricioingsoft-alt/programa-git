
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.pagina_login, name='login'),
    path('registro/', views.pagina_registro, name='registro'),
    path('panel/', views.panel, name='panel'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]
