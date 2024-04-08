"""Event handlers for the Open edX Unidigital plugin."""

import logging
from typing import List

from django.conf import settings

from openedx_unidigital.edxapp_wrapper.course_groups import CourseUserGroup
from openedx_unidigital.edxapp_wrapper.course_groups import add_user_to_cohort as add_user_to_cohort_backend
from openedx_unidigital.edxapp_wrapper.course_groups import get_cohort_by_id
from openedx_unidigital.edxapp_wrapper.lang_pref import LANGUAGE_KEY
from openedx_unidigital.edxapp_wrapper.modulestore import modulestore
from openedx_unidigital.edxapp_wrapper.student import get_user_by_username_or_email
from openedx_unidigital.edxapp_wrapper.teams import (
    AddToIncompatibleTeamError,
    AlreadyOnTeamInTeamset,
    NotEnrolledInCourseForTeam,
    get_team_by_team_id,
)
from openedx_unidigital.edxapp_wrapper.user_preferences import get_user_preference

log = logging.getLogger(__name__)


def add_member_to_course_group_by_language(enrollment, **kwargs) -> None:
    """
    Add user to course group (team/cohort) by language preference.

    - First, we get the configuration per language stored in other course settings.
    - Then, we get the user's language preference.
    - Finally, we add the user to the course group based on the user's language preference.

    Args:
        enrollment (CourseEnrollment): The course enrollment object.
        **kwargs: Kwargs of the event.
    """
    course_key = enrollment.course.course_key

    membership_by_language = get_membership_by_language(course_key)
    user = get_user_by_username_or_email(enrollment.user.pii.username)
    lang_pref = get_language_preference(user)

    if lang_pref in membership_by_language:
        add_user_to_course_group(user, membership_by_language[lang_pref], course_key)


def add_user_to_course_group(user, course_groups: List[dict], course_key: str) -> None:
    """
    Add user to course group.

    Args:
        user (User): The user object.
        course_groups (List[dict]): The course groups of the language.
        course_key (str): The course key.
    """
    for group in course_groups:
        group_id = group.get("id", "")
        if group.get("type") == "team":
            add_user_to_team(user, group_id)
        elif group.get("type") == "cohort":
            add_user_to_cohort(user, group_id, course_key)


def get_language_preference(user) -> str:
    """
    Get the user's language preference.

    Args:
        user (User): The user object.

    Returns:
        str: The user's language preference.
    """
    return get_user_preference(user, LANGUAGE_KEY) or settings.LANGUAGE_CODE


def get_membership_by_language(course_key: str) -> dict:
    """
    Get the other course settings for a course.

    Args:
        course_key (str): The course key.

    Returns:
        dict: The other course settings if exists, otherwise an empty dict.
    """
    course_block = modulestore().get_course(course_key)
    return course_block.other_course_settings.get("MEMBERSHIP_BY_LANGUAGE_CONFIG") or {}


def add_user_to_team(user, team_id: str) -> None:
    """
    Add a user to a team.

    Args:
        user (User): The user object.
        team_id (str): The team id.
    """
    team = get_team_by_team_id(team_id)

    if team:
        try:
            team.add_user(user)
            log.info(f"The user='{user}' has been added to the team='{team}'.")
        except AlreadyOnTeamInTeamset:
            log.info(f"The user='{user}' is already on a team in the teamset.")
        except NotEnrolledInCourseForTeam:
            log.info(f"The user='{user}' is not enrolled in the course of the team.")
        except AddToIncompatibleTeamError:
            log.info(f"The user='{user}' cannot be added to the team.")
    else:
        log.info(f"The team with the {team_id=} does not exist.")


def add_user_to_cohort(user, cohort_id: str, course_key: str) -> None:
    """
    Add a user to a cohort.

    Args:
        user (User): The user object.
        cohort_id (str): The cohort id.
        course_key (str): The course key.
    """
    try:
        cohort = get_cohort_by_id(course_key, cohort_id)
        add_user_to_cohort_backend(cohort, user)
        log.info(f"The user='{user}' has been added to the cohort='{cohort}'.")
    except CourseUserGroup.DoesNotExist:
        log.info(f"The cohort with the {cohort_id=} does not exist.")
    except ValueError:
        log.info(f"The user='{user}' is already in the cohort.")
