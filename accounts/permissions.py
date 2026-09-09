from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def role_required(*roles):
    """Restrict a view to users whose role is in `roles` and who are approved."""

    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.role not in roles:
                raise PermissionDenied("You do not have access to this page.")
            if user.needs_approval:
                raise PermissionDenied("Your account is pending Administrator approval.")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
