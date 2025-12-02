from functools import wraps
from django.shortcuts import redirect

# Requiere sesión activa
def usuario_login_requerido(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "usuario_id" not in request.session:
            return redirect("logearse")
        return view_func(request, *args, **kwargs)
    return wrapper


# Requiere uno o varios roles permitidos
def rol_requerido(roles_permitidos):
    if isinstance(roles_permitidos, str):
        roles_permitidos = [roles_permitidos]

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # Verifica sesión
            if "usuario_id" not in request.session:
                return redirect("logearse")

            rol_usuario = request.session.get("usuario_rol", None)

            if rol_usuario not in roles_permitidos:
                return redirect("home")  # ACCESO DENEGADO

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
