"""Event handlers for the Open edX Unidigital plugin."""

from xmodule.modulestore.django import modulestore
from django.conf import settings
from crum import get_current_request

from openedx.core.djangoapps.user_api.preferences.api import get_user_preference

from openedx.core.djangoapps.lang_pref import LANGUAGE_KEY


def add_member_to_team_by_language(signal, sender, enrollment, metadata, **kwargs):
    """
    Membership by language configuration.

    Args:
        signal (_type_): _description_
        sender (_type_): _description_
        enrollment (_type_): _description_
        metadata (_type_): _description_
    """
    course_key = enrollment.course.course_key
    course_block = modulestore().get_course(course_key)
    membership_by_language = course_block.other_course_settings.get(
        "MEMBERSHIP_BY_LANGUAGE_CONFIG"
    )
    request = get_current_request()
    user = request.user
    language_preference = get_user_preference(user, LANGUAGE_KEY)
