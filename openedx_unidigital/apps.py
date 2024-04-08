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
        'settings_config': {
            'lms.djangoapp': {
                'test': {'relative_path': 'settings.test'},
                'common': {'relative_path': 'settings.common'},
                'production': {'relative_path': 'settings.production'},
            },
        },
    }

    def ready(self):
        from openedx_unidigital.roles import CourseStaffRoleMonkeyPatched
        import common.djangoapps.student.roles as roles_module
        print("Monkey patching RoleBase -----------------------")
        roles_module.CourseStaffRole = CourseStaffRoleMonkeyPatched
        print("Monkey patched RoleBase ------------------------")
        import common.djangoapps.student.roles as roles_module
        print(roles_module.CourseStaffRole)
