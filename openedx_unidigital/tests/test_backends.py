"""Test suite for auth backends for the Open edX Unidigital plugin."""

from unittest import TestCase
from unittest.mock import Mock, patch

from openedx_unidigital.backends import UnidigitalRulesBackend


class TestUnidigitalRulesBackend(TestCase):
    """Test suite for the UnidigitalRulesBackend class."""

    def setUp(self):
        """Set up the test suite."""
        self.backend = UnidigitalRulesBackend()
        self.user = Mock()

    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=False,
    )
    def test_no_access_rule_permission_backend(self, *_):
        """Test auth backend when the user does not have access according to the RulePermissionBackend.

        Expected behavior:
        - The method should return False.
        """
        self.assertFalse(self.backend.has_perm(self.user, "perm"))

    @patch(
        "openedx_unidigital.backends.CourseTeamInstructor.get_teams_for_user",
        return_value=[2, 3],
    )
    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="POST",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    @patch("openedx_unidigital.backends.CourseTeamMembership")
    def test_access_based_on_student_teams_and_instructor_teams(
        self, mock_course_team_membership, *_
    ):
        """Test auth backend when the user has access according to the RulePermissionBackend.

        In this case, we need to check for the student teams and the instructor teams.

        Expected behavior:
        - The method should return True.
        """
        mock_course_team_membership.objects.filter.return_value.values_list.return_value = {
            1,
            2,
        }

        self.assertTrue(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.CourseTeamInstructor.get_teams_for_user",
        return_value=[3],
    )
    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="POST",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    @patch("openedx_unidigital.backends.CourseTeamMembership")
    def test_access_based_on_teams_no_conditions_met(
        self, mock_course_team_membership, *_
    ):
        """Test auth backend when the user and instructor teams do not match.

        Expected behavior:
        - The method should return False denying the access.
        """
        mock_course_team_membership.objects.filter.return_value.values_list.return_value = {
            1,
            2,
        }

        self.assertFalse(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="POST",
            path="/student/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    def test_access_based_on_teams_no_path(self, *_):
        """Test auth backend when the path is not the monitored one.

        Expected behavior:
        - The method should return True allowing the access.
        """
        self.assertTrue(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value=None)),
            method="POST",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    def test_access_based_on_teams_no_post_student(self, *_):
        """Test auth backend when the post student is not present.

        Expected behavior:
        - The method should return True allowing the access.
        """
        self.assertTrue(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="GET",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    def test_access_based_on_teams_different_perm(self, *_):
        """Test auth backend when the permission is different from the monitored ones.

        Expected behavior:
        - The method should return True allowing the access.
        """
        self.assertTrue(
            self.backend.has_perm(
                self.user, "ANOTHER_PERM", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.CourseTeamInstructor.get_teams_for_user",
        return_value=[3],
    )
    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="POST",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    @patch("openedx_unidigital.backends.CourseTeamMembership")
    def test_access_based_on_teams_no_student_teams(
        self, mock_course_team_membership, *_
    ):
        """Test auth backend when the student does not have teams.

        Expected behavior:
        - The method should return False denying the access.
        """
        mock_course_team_membership.objects.filter.return_value.values_list.return_value = {
            1,
            2,
        }

        self.assertFalse(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )

    @patch(
        "openedx_unidigital.backends.CourseTeamInstructor.get_teams_for_user",
        return_value=[],
    )
    @patch(
        "openedx_unidigital.backends.get_current_request",
        return_value=Mock(
            POST=Mock(get=Mock(return_value="unique_student_identifier")),
            method="POST",
            path="/instructor/api/",
        ),
    )
    @patch(
        "openedx_unidigital.backends.RulePermissionBackend.has_perm",
        return_value=True,
    )
    @patch("openedx_unidigital.backends.CourseTeamMembership")
    def test_access_based_on_teams_no_instructor_teams(
        self, mock_course_team_membership, *_
    ):
        """Test auth backend when the instructor does not have teams.

        Expected behavior:
        - The method should return True allowing the access cause the instructor
        is not part of any team.
        """
        mock_course_team_membership.objects.filter.return_value.values_list.return_value = {
            1,
            2,
        }

        self.assertTrue(
            self.backend.has_perm(
                self.user, "VIEW_ENROLLMENTS", Mock(course_id="course_id")
            )
        )
