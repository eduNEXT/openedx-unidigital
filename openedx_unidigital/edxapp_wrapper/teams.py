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


def get_already_on_team_in_teamset_error():
    """
    Wrapper for `teams.errors.AlreadyOnTeamInTeamset`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.AlreadyOnTeamInTeamset


def get_not_enrolled_in_course_for_team_error():
    """
    Wrapper for `teams.errors.NotEnrolledInCourseForTeam`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.NotEnrolledInCourseForTeam


def get_add_to_incompatible_team_error():
    """
    Wrapper for `teams.errors.AddToIncompatibleTeamError`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.AddToIncompatibleTeamError


def get_course_team_membership_model():
    """
    Wrapper for `teams.models.CourseTeamMembership`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.CourseTeamMembership


def get_teams_in_teamset(*args, **kwargs):
    """
    Wrapper for `teams.api.get_teams_in_teamset`
    """
    backend_function = settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND
    backend = import_module(backend_function)

    return backend.get_teams_in_teamset(*args, **kwargs)


AddToIncompatibleTeamError = get_add_to_incompatible_team_error()
AlreadyOnTeamInTeamset = get_already_on_team_in_teamset_error()
NotEnrolledInCourseForTeam = get_not_enrolled_in_course_for_team_error()
CourseTeamMembership = get_course_team_membership_model()
