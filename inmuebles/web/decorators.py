from django.http import HttpResponseRedirect
from functools import wraps
from django.shortcuts import redirect

def tipo_usuario_required(request_tipo_usuario:str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                tipo_usuario = getattr(request.user, 'tipo_usuario', None)
                if tipo_usuario and getattr(tipo_usuario, 'nombre_tipo_usuario', None) == request_tipo_usuario:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('not_authorized')  # Change this to your 'not authorized' view
            else:
                return redirect('login')
        return _wrapped_view
    return decorator

