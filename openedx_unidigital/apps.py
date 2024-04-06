"""
openedx_unidigital Django application initialization.
"""

from django.apps import AppConfig


class OpenedxUnidigitalConfig(AppConfig):
    """
    Configuration for the openedx_unidigital Django application.
    """

    name = "openedx_unidigital"

    plugin_app = {
        "signals_config": {
            "lms.djangoapp": {
                "relative_path": "handlers",
                "receivers": [
                    {
                        "receiver_func_name": "add_member_to_team_by_language",
                        "signal_path": "openedx_events.learning.signals.COURSE_ENROLLMENT_CREATED",
                    },
                ],
            }
        },
    }
