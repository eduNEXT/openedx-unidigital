"""
Lang Pref generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def get_language_key_constant():
    """
    Wrapper for `openedx.core.djangoapps.lang_pref.LANGUAGE_KEY`.
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND
    backend = import_module(backend_function)

    return backend.LANGUAGE_KEY


LANGUAGE_KEY = get_language_key_constant()
