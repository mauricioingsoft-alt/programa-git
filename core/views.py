from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response


def inicio(request):
    return HttpResponse("Mi proyecto Django funciona correctamente")


@api_view(['POST'])
def registro(request):
    return Response({
        'mensaje': 'El servicio de registro funciona correctamente'
    })
