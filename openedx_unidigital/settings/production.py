"""
Production settings for the plugin.
"""


def plugin_settings(settings):
    """
    Set of plugin settings used by the Open Edx platform.
    More info: https://github.com/edx/edx-platform/blob/master/openedx/core/djangoapps/plugins/README.rst
    """
    settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND",
        settings.OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND,
    )
    settings.OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND",
        settings.OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND,
    )
    settings.OPENEDX_UNIDIGITAL_MODULESTORE_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "OPENEDX_UNIDIGITAL_MODULESTORE_BACKEND",
        settings.OPENEDX_UNIDIGITAL_MODULESTORE_BACKEND,
    )
    settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND = getattr(settings, "ENV_TOKENS", {}).get(
        "OPENEDX_UNIDIGITAL_TEAMS_BACKEND",
        settings.OPENEDX_UNIDIGITAL_TEAMS_BACKEND,
    )
    settings.OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND = getattr(
        settings, "ENV_TOKENS", {}
    ).get(
        "OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND",
        settings.OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND,
    )
