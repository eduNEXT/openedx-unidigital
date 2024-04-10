"""
Settings for the LimeSurvey plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    if settings.SERVICE_VARIANT == 'lms':
        settings.AUTHENTICATION_BACKENDS.append('openedx_unidigital.roles.UnidigitalRulesBackend')
        settings.AUTHENTICATION_BACKENDS.remove('bridgekeeper.backends.RulePermissionBackend')
