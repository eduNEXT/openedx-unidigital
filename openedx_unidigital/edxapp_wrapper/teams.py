"""
Teams generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_team_by_team_id(*args, **kwargs):
    """
    Wrapper for `teams.api.get_team_by_team_id`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.get_team_by_team_id(*args, **kwargs)
