from common.djangoapps.student.models import CourseAccessRole
from common.djangoapps.student.roles import CourseStaffRole, RoleCache
from crum import get_current_request, get_current_user
from pprint import pprint

class CourseStaffRoleMonkeyPatched(CourseStaffRole):
    """
    Roles by type (e.g., instructor, beta_user) and optionally org, course_key
    """

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
        if check_user_activation and not (user.is_authenticated and user.is_active):
            return False

        print("JUGANDO2 CON PERMISOS en RoleBase.has_user")

        original_return_value = user._roles.has_role(self._role_name, self.course_key, self.org)

        crum_request = get_current_request()
        crum_user = get_current_user()
        post_student = crum_request.POST.get("unique_student_identifier", crum_request.POST.get("student", None))

        if all([
                "/instructor/api/" in crum_request.path,
                original_return_value == True,
                crum_request.method == 'POST',
                self._role_name == "staff", # como podriamos validar que es 'limited staff' y no solo 'staff'
                post_student,
            ]):

            print("JUGANDO CON PERMISOS en RoleBase.has_user")
            print(original_return_value)
            pprint(post_student)
            pprint(self._role_name)
            pprint(crum_request.POST)
            pprint(self)
            # pprint(dir(self))

            if post_student == "felipe":  # voy a bloquear que limited no pueda alterar a 'felipe'
                return False

        # pylint: disable=protected-access
        if not hasattr(user, '_roles'):
            # Cache a list of tuples identifying the particular roles that a user has
            # Stored as tuples, rather than django models, to make it cheaper to construct objects for comparison
            user._roles = RoleCache(user)

        return original_return_value
