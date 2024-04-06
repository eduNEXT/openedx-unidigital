"""Event handlers for the Open edX Unidigital plugin."""

from crum import get_current_request
from django.conf import settings

from openedx_unidigital.edxapp_wrapper.course_groups import add_user_to_cohort
from openedx_unidigital.edxapp_wrapper.lang_pref import LANGUAGE_KEY
from openedx_unidigital.edxapp_wrapper.modulestore import modulestore
from openedx_unidigital.edxapp_wrapper.teams import get_team_by_team_id
from openedx_unidigital.edxapp_wrapper.user_preferences import get_user_preference


def add_member_to_team_by_language(
    signal, sender, enrollment, metadata, **kwargs
) -> None:
    """
    Add user to team/cohort by language.
    """
    course_key = enrollment.course.course_key
    course_block = modulestore().get_course(course_key)
    membership_by_language = course_block.other_course_settings.get(
        "MEMBERSHIP_BY_LANGUAGE_CONFIG"
    )
    request = get_current_request()
    user = request.user
    language_preference = (
        get_user_preference(user, LANGUAGE_KEY) or settings.LANGUAGE_CODE
    )

    if language_preference in membership_by_language:
        course_groups = membership_by_language[language_preference]
        for group in course_groups:
            if group["type"] == "team":
                add_user_to_team(user, group["id"])
            elif group["type"] == "cohort":
                add_user_to_cohort(user, group["id"])


def add_user_to_team(user, team_id: str) -> None:
    """
    Add user to team.

    Args:
        user (User): The user object.
        team_id (str): The team id.
    """
    team = get_team_by_team_id(team_id)
    team.add_user(user)
