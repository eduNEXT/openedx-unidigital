"""Event handlers for the Open edX Unidigital plugin."""

import logging
from typing import Dict, List

from django.conf import settings

from openedx_unidigital.edxapp_wrapper.course_groups import CourseUserGroup
from openedx_unidigital.edxapp_wrapper.course_groups import add_user_to_cohort as add_user_to_cohort_backend
from openedx_unidigital.edxapp_wrapper.course_groups import get_cohort_by_name
from openedx_unidigital.edxapp_wrapper.lang_pref import LANGUAGE_KEY
from openedx_unidigital.edxapp_wrapper.modulestore import modulestore
from openedx_unidigital.edxapp_wrapper.student import get_user_by_username_or_email
from openedx_unidigital.edxapp_wrapper.teams import (
    AddToIncompatibleTeamError,
    AlreadyOnTeamInTeamset,
    CourseTeamMembership,
    NotEnrolledInCourseForTeam,
    get_team_by_team_id,
)
from openedx_unidigital.edxapp_wrapper.user_preferences import get_user_preference

log = logging.getLogger(__name__)


def add_member_to_course_group_by_language(enrollment, **kwargs) -> None:
    """
    Add user to course group (team/cohort) by language preference.

    If the language preference of the user does not exist in the configuration,
    the user will be added to the default group if it exists.

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

    course_groups = membership_by_language.get(
        lang_pref, membership_by_language.get("default")
    )
    if course_groups:
        add_user_to_course_group(user, course_groups, course_key)


def add_user_to_course_group(user, course_groups: List[dict], course_key: str) -> None:
    """
    Add user to course group.

    Args:
        user (User): The user object.
        course_groups (List[dict]): The course groups of the language.
        course_key (str): The course key.
    """
    for group in course_groups:
        group_type = group.get("type", "").lower()
        group_id = group.get("id", "")
        if group_type == "team":
            add_user_to_team(user, group_id)
        elif group_type == "cohort":
            add_user_to_cohort(user, group_id, course_key)


def get_language_preference(user) -> str:
    """
    Get the user's language preference.

    If the user's language preference is not set, the default
    language of the platform will be used.

    Args:
        user (User): The user object.

    Returns:
        str: The user's language preference.
    """
    return get_user_preference(user, LANGUAGE_KEY) or settings.LANGUAGE_CODE


def get_membership_by_language(course_key: str) -> dict:
    """
    Get the other course settings for a course.

    If the key of the dictionary is a comma-separated list of languages,
    it will be parsed and added to new dictionary in a separate key.

    Args:
        course_key (str): The course key.

    Returns:
        dict: The other course settings if exists, otherwise an empty dict.
    """
    course_block = modulestore().get_course(course_key)
    membership_by_language: Dict[str, list] = (
        course_block.other_course_settings.get("MEMBERSHIP_BY_LANGUAGE_CONFIG") or {}
    )

    parsed_dict = {}
    for lang, groups in membership_by_language.items():
        langs_list = lang.split(",")
        for language in langs_list:
            parsed_dict[language.lower()] = groups

    return parsed_dict


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
            log.debug(f"The user='{user}' has been added to the team='{team}'.")
        except AlreadyOnTeamInTeamset:
            old_membership = CourseTeamMembership.objects.filter(
                user=user,
                team__course_id=team.course_id,
                team__topic_id=team.topic_id,
            ).first()
            old_membership.delete()
            team.add_user(user)
            log.debug(
                f"The user='{user}' was moved from the "
                f"team='{old_membership.team}' to the team='{team}'."
            )
        except NotEnrolledInCourseForTeam:
            log.exception(
                f"The user='{user}' is not enrolled in the course of the team."
            )
        except AddToIncompatibleTeamError:
            log.exception(f"The user='{user}' cannot be added to the team.")
    else:
        log.exception(f"The team with the {team_id=} does not exist.")


def add_user_to_cohort(user, cohort_name: str, course_key: str) -> None:
    """
    Add a user to a cohort.

    Args:
        user (User): The user object.
        cohort_name (str): The cohort name.
        course_key (str): The course key.
    """
    try:
        cohort = get_cohort_by_name(course_key, cohort_name)
        add_user_to_cohort_backend(cohort, user)
        log.debug(f"The user='{user}' has been added to the cohort='{cohort}'.")
    except CourseUserGroup.DoesNotExist:
        log.exception(f"The cohort with the {cohort_name=} does not exist.")
    except ValueError:
        log.exception(f"The user='{user}' is already in the cohort.")
