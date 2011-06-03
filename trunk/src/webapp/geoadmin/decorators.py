def admin_required(func):
    def _wrapper(*args, **kwargs):
        session = args[0].session#request es el primer parametro que pasamos
        if session.get('user'):
            if session['user'].is_admin():
                return func(*args, **kwargs)

        from django.core.exceptions import PermissionDenied
        raise PermissionDenied()
    return _wrapper