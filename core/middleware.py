from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.utils.decorators import method_decorator


def admin_required(view_func):
    """
    Decorator for views that require admin privileges
    """
    return user_passes_test(
        lambda u: u.is_superuser or u.username in getattr(settings, 'ADMIN_USERS', []),
        login_url='/admin/login/',
        redirect_field_name=None
    )(view_func)


class AdminOnlyContentMiddleware:
    """
    Middleware to restrict content modification to admin users only
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that should be restricted to admin only
        self.restricted_paths = [
            '/admin/',  # Django admin
            '/research/',  # Research paper management (if not using admin)
        ]

    def __call__(self, request):
        # Check if admin-only content restriction is enabled
        if not getattr(settings, 'ADMIN_ONLY_CONTENT', False):
            return self.get_response(request)

        # Allow access to login pages and static/media files
        if (request.path.startswith('/admin/login/') or
            request.path.startswith('/static/') or
            request.path.startswith('/media/') or
            request.path.startswith('/api/quran/') or  # Allow Quran API access
            request.method in ['GET', 'HEAD']):  # Allow read-only access
            return self.get_response(request)

        # Check if user is authenticated and is admin
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())

        # Check if user is admin
        is_admin = (
            request.user.is_superuser or
            request.user.username in getattr(settings, 'ADMIN_USERS', [])
        )

        if not is_admin:
            # For non-admin users, restrict write operations
            if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
                return HttpResponseForbidden(
                    "Content modification is restricted to administrators only."
                )

        return self.get_response(request)
