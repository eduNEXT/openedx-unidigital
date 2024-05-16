"""Xmodule generalized definitions."""

from importlib import import_module

from django.conf import settings


def get_teams_configuration_service():
    """
    Wrapper for `xmodule.services.TeamsConfigurationService`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_XMODULE_BACKEND
    backend = import_module(backend_function)

    return backend.TeamsConfigurationService


TeamsConfigurationService = get_teams_configuration_service()
