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
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if "usuario_id" not in request.session:
                return redirect("logearse")

            rol_actual = request.session.get("usuario_rol")

            if isinstance(roles_permitidos, list):
                if rol_actual not in roles_permitidos:
                    return redirect("home")
            else:
                if rol_actual != roles_permitidos:
                    return redirect("home")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

