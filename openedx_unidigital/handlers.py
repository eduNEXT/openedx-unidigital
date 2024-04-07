"""Event handlers for the Open edX Unidigital plugin."""

from typing import List

from django.conf import settings

from openedx_unidigital.edxapp_wrapper.course_groups import add_user_to_cohort
from openedx_unidigital.edxapp_wrapper.lang_pref import LANGUAGE_KEY
from openedx_unidigital.edxapp_wrapper.modulestore import modulestore
from openedx_unidigital.edxapp_wrapper.student import get_user_by_username_or_email
from openedx_unidigital.edxapp_wrapper.teams import get_team_by_team_id
from openedx_unidigital.edxapp_wrapper.user_preferences import get_user_preference


def add_member_to_course_group_by_language(enrollment, **kwargs) -> None:
    """
    Add user to team/cohort by language.
    """
    membership_by_language = get_membership_by_language(enrollment.course.course_key)
    user = get_user_by_username_or_email(enrollment.user.pii.username)
    language_preference = get_language_preference(user)

    if language_preference in membership_by_language:
        add_user_to_course_group(user, membership_by_language[language_preference])


def add_user_to_course_group(user, course_groups: List[dict]) -> None:
    """
    Add user to course group.

    Args:
        user (User): The user object.
        course_groups (List[dict]): The course groups.
    """
    for group in course_groups:
        group_id = group.get("id", "")
        if group.get("type") == "team":
            add_user_to_team(user, group_id)
        elif group.get("type") == "cohort":
            add_user_to_cohort(user, group_id)


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
        dict: The other course settings.
    """
    course_block = modulestore().get_course(course_key)
    return course_block.other_course_settings.get("MEMBERSHIP_BY_LANGUAGE_CONFIG")


def add_user_to_team(user, team_id: str) -> None:
    """
    Add user to team.

    Args:
        user (User): The user object.
        team_id (str): The team id.
    """
    team = get_team_by_team_id(team_id)
    team.add_user(user)
