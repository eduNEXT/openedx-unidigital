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

    return backend.add_user_to_cohort(*args, **kwargs)


def get_cohort_by_name(*args, **kwargs):
    """
    Wrapper for `openedx.core.djangoapps.course_groups.cohorts.get_cohort_by_name`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND
    backend = import_module(backend_function)

    return backend.get_cohort_by_name(*args, **kwargs)


def get_course_user_group_model():
    """
    Wrapper for `openedx.core.djangoapps.course_groups.models.CourseUserGroup`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND
    backend = import_module(backend_function)

    return backend.CourseUserGroup


CourseUserGroup = get_course_user_group_model()
