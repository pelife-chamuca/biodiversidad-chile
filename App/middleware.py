from .models import Usuario

def usuario_middleware(get_response):
    def middleware(request):
        usuario_id = request.session.get('usuario_id')
        if usuario_id:
            try:
                request.usuario = Usuario.objects.get(pk=usuario_id)
            except Usuario.DoesNotExist:
                request.usuario = None
        else:
            request.usuario = None
        return get_response(request)
    return middleware