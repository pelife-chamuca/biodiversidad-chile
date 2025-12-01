from functools import wraps
from django.shortcuts import redirect

# Control de sesión personalizada
def usuario_login_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('logearse')
        return view_func(request, *args, **kwargs)
    return wrapper


# Control de rol específico
def rol_requerido(rol_permitido):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'usuario_id' not in request.session:
                return redirect('logearse')

            usuario_rol = request.session.get('usuario_rol', None)
            if usuario_rol != rol_permitido:
                # No tiene permisos -> redirigir o mostrar error
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
