"""Authentication backends for the Unidigital project."""

from bridgekeeper.backends import RulePermissionBackend
from crum import get_current_request
from django.conf import settings
from opaque_keys.edx.keys import CourseKey

from openedx_unidigital.edxapp_wrapper.instructor import (
    ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM,
    ENROLLMENT_REPORT,
    GIVE_STUDENT_EXTENSION,
    OVERRIDE_GRADES,
    VIEW_ENROLLMENTS,
)
from openedx_unidigital.edxapp_wrapper.student import CourseLimitedStaffRole
from openedx_unidigital.edxapp_wrapper.teams import CourseTeamMembership
from openedx_unidigital.models import CourseTeamInstructor


class UnidigitalRulesBackend(RulePermissionBackend):
    """Backend for the Unidigital project based on custom business rules."""

    def has_perm(self, user, perm, obj=None):
        """
        Check if the user has the permission to perform the action.

        For a set of specified permissions, the user must be an instructor
        of the team that the student is part of.
        """
        has_perm_access = super().has_perm(user, perm, obj)

        if not settings.ENABLE_UNIDIGITAL_AUTH_RULES_BACKEND:
            return has_perm_access

        if perm not in [
            ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM,
            ENROLLMENT_REPORT,
            GIVE_STUDENT_EXTENSION,
            OVERRIDE_GRADES,
            VIEW_ENROLLMENTS,
        ]:
            return has_perm_access

        if not CourseLimitedStaffRole(obj.course_id).has_user(user):
            return has_perm_access

        if not isinstance(has_perm_access, bool):
            has_perm_access = has_perm_access.has_access

        if not has_perm_access:
            return False

        has_team_access = True
        crum_request = get_current_request()
        post_student = crum_request.POST.get(
            "unique_student_identifier",
            crum_request.POST.get("student", None),
        )
        if all(
            [
                "/instructor/api/" in crum_request.path,
                crum_request.method == "POST",
                post_student,
            ]
        ):
            student_teams = CourseTeamMembership.objects.filter(
                user_id=user.id,
                team__course_id=obj.course_id,
            ).values_list("team_id", flat=True)
            instructor_teams = CourseTeamInstructor.get_teams_for_user(user.username)
            if not instructor_teams:
                return True
            has_team_access = bool(student_teams.intersection(instructor_teams))

        return has_team_access
