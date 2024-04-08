"""
These settings are here to use during tests, because django requires them.

In a real-world use case, apps in this project are installed into other
Django applications, so these settings will not be used.
"""

from os.path import abspath, dirname, join


def root(*args):
    """
    Get the absolute path of the given path relative to the project root.
    """
    return join(abspath(dirname(__file__)), *args)


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "default.db",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    }
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "openedx_unidigital",
)

LOCALE_PATHS = [
    root("openedx_unidigital", "conf", "locale"),
]

SECRET_KEY = "insecure-secret-key"

MIDDLEWARE = (
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": False,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",  # this is required for admin
                "django.contrib.messages.context_processors.messages",  # this is required for admin
            ],
        },
    }
]

# Settings for the plugin
OPENEDX_UNIDIGITAL_COURSE_GROUPS_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.course_groups_q_v1_test"
)
OPENEDX_UNIDIGITAL_LANG_PREF_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.lang_pref_q_v1_test"
)
OPENEDX_UNIDIGITAL_MODULESTORE_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.modulestore_q_v1_test"
)
OPENEDX_UNIDIGITAL_TEAMS_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.teams_q_v1_test"
)
OPENEDX_UNIDIGITAL_USER_PREFERENCES_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.user_preferences_q_v1_test"
)
OPENEDX_UNIDIGITAL_STUDENT_BACKEND = (
    "openedx_unidigital.edxapp_wrapper.backends.student_q_v1_test"
)
