"""
Course Groups generalized definitions.
"""

from importlib import import_module

from django.conf import settings


def add_user_to_cohort(*args, **kwargs):
    """
    Wrapper for `openedx.core.djangoapps.course_groups.cohorts.add_user_to_cohort`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND
    backend = import_module(backend_function)

    return backend.modulestore(*args, **kwargs)
