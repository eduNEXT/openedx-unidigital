"""
Common settings for the plugin.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.course_groups_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.lang_pref_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_MODULESTORE_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.modulestore_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.teams_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.user_preferences_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_STUDENT_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.student_q_v1"
    )
