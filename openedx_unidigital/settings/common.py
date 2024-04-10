"""
Settings for the LimeSurvey plugin.
"""


def plugin_settings(settings):
    """
    Read / Update necessary common project settings.
    """
    if settings.SERVICE_VARIANT == 'lms':
        settings.AUTHENTICATION_BACKENDS = [
            'rules.permissions.ObjectPermissionBackend',
            'django.contrib.auth.backends.AllowAllUsersModelBackend',
            'openedx_unidigital.backends.UnidigitalRulesBackend'
        ]
