"""
User Preferences generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_user_preference(*args, **kwargs):
    """
    Wrapper for `openedx.core.djangoapps.user_api.preferences.api.get_user_preference`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_preference(*args, **kwargs)
