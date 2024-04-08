from common.djangoapps.student.models import CourseAccessRole
from common.djangoapps.student.roles import CourseStaffRole

class CourseStaffRoleMonkeyPatched(CourseStaffRole):
    """
    Roles by type (e.g., instructor, beta_user) and optionally org, course_key
    """

    # pylint: disable=arguments-differ
    def has_user(self, user, check_user_activation=True):
        """
        Check if the supplied django user has access to this role.

        Arguments:
            user: user to check against access to role
            check_user_activation: Indicating whether or not we need to check
                user activation while checking user roles
        Return:
            bool identifying if user has that particular role or not
        """
        print("HAS USER MONKEY PATCHED -------------------------------------")
        import pudb; pudb.set_trace()
        if check_user_activation and not (user.is_authenticated and user.is_active):
            return False

        if CourseAccessRole.objects.filter(user=user, role='limited_staff').exists():
            print("USER IS LIMITED STAFF -------------------------------------")
        # # pylint: disable=protected-access
        # if not hasattr(user, '_roles'):
        #     # Cache a list of tuples identifying the particular roles that a user has
        #     # Stored as tuples, rather than django models, to make it cheaper to construct objects for comparison
        #     user._roles = RoleCache(user)

        return user._roles.has_role(self._role_name, self.course_key, self.org)
