"""
User Preferences generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_user_preference(*args, **kwargs):
    """
    Wrapper for `teams.api.get_team_by_team_id`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND
    backend = import_module(backend_function)

    return backend.get_user_preference(*args, **kwargs)
