"""
Common settings for the plugin.
"""

from openedx_unidigital import ROOT_DIRECTORY


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
    settings.OPENEDX_UNIDIGITAL_INSTRUCTOR_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.instructor_q_v1"
    )
    settings.OPENEDX_UNIDIGITAL_XMODULE_BACKEND = (
        "openedx_unidigital.edxapp_wrapper.backends.xmodule_q_v1"
    )
    if settings.SERVICE_VARIANT == "lms":
        settings.AUTHENTICATION_BACKENDS.append(
            "openedx_unidigital.backends.UnidigitalRulesBackend"
        )
        settings.AUTHENTICATION_BACKENDS.remove(
            "bridgekeeper.backends.RulePermissionBackend"
        )
    settings.ENABLE_UNIDIGITAL_AUTH_RULES_BACKEND = getattr(settings, "ENABLE_UNIDIGITAL_AUTH_RULES_BACKEND", True)
    settings.MAKO_TEMPLATE_DIRS_BASE.append(ROOT_DIRECTORY / "templates")
