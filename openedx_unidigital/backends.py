"""Authentication backends for the Unidigital project."""

from bridgekeeper.backends import RulePermissionBackend
from crum import get_current_request

from openedx_unidigital.edxapp_wrapper.instructor import (
    ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM,
    ENROLLMENT_REPORT,
    GIVE_STUDENT_EXTENSION,
    OVERRIDE_GRADES,
    VIEW_ENROLLMENTS,
)
from openedx_unidigital.edxapp_wrapper.teams import CourseTeamMembership
from openedx_unidigital.models import CourseTeamInstructor


class UnidigitalRulesBackend(RulePermissionBackend):
    """Backend for the Unidigital project based on custom business rules."""

    def has_perm(self, user, perm, obj=None):
        """Check if the user has the permission to perform the action.

        For a set of specified permissions, the user must be an instructor
        of the team that the student is part of.
        """
        has_perm_access = super().has_perm(user, perm, obj)

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
                perm
                in [
                    GIVE_STUDENT_EXTENSION,
                    VIEW_ENROLLMENTS,
                    ENROLLMENT_REPORT,
                    OVERRIDE_GRADES,
                    ALLOW_STUDENT_TO_BYPASS_ENTRANCE_EXAM,
                ],
                post_student,
            ]
        ):
            student_teams = CourseTeamMembership.objects.filter(
                user_id=user.id,
                team__course_id=obj.course_id,
            ).values_list("team_id", flat=True)
            instructor_teams = CourseTeamInstructor.get_teams_for_user(user.username)
            has_team_access = bool(student_teams.intersection(instructor_teams))

        return has_team_access
