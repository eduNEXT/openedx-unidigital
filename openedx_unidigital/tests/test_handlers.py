"""Tests for handlers of the Open edX Unidigital plugin"""

from unittest import TestCase
from unittest.mock import Mock, patch

from django.core.exceptions import ObjectDoesNotExist

from openedx_unidigital.handlers import (
    add_member_to_course_group_by_language,
    add_user_to_cohort,
    add_user_to_course_group,
    add_user_to_team,
    get_language_preference,
    get_membership_by_language,
)

HANDLERS_MODULE_PATH = "openedx_unidigital.handlers"
LANGUAGE_KEY = "pref-lang"


class AlreadyOnTeamInTeamset(BaseException):
    pass


class AddToIncompatibleTeamError(BaseException):
    pass


class NotEnrolledInCourseForTeam(BaseException):
    pass


class UserMock:
    """Mock class for User"""

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return self.username


class TestHandlers(TestCase):
    """Tests for handlers of the Open edX Unidigital plugin"""

    def setUp(self) -> None:
        self.enrollment = Mock()
        self.course_key = "test-course-key"
        self.username = "test-username"
        self.team = Mock(id="team-id")
        self.cohort = Mock(id="cohort-name")
        self.enrollment.course.course_key = self.course_key
        self.enrollment.user.pii.username = self.username
        self.user = UserMock(self.username)
        self.lang_pref = "en"
        self.membership_by_lang_conf = {
            "en": [
                {"type": "team", "id": "team-id"},
                {"type": "cohort", "id": "cohort-name"},
            ]
        }
        self.other_course_settings = {
            "MEMBERSHIP_BY_LANGUAGE_CONFIG": self.membership_by_lang_conf
        }
        self.course = Mock(
            other_course_settings=self.other_course_settings,
        )

    @patch(f"{HANDLERS_MODULE_PATH}.get_membership_by_language")
    @patch(f"{HANDLERS_MODULE_PATH}.get_user_by_username_or_email")
    @patch(f"{HANDLERS_MODULE_PATH}.get_language_preference")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_course_group")
    def test_add_member_to_course_group_by_language(
        self,
        mock_add_user_to_course_group: Mock,
        mock_get_language_preference: Mock,
        mock_get_user_by_username_or_email: Mock,
        mock_get_membership_by_language: Mock,
    ):
        """Test `add_member_to_course_group_by_language` with group for language"""
        mock_get_user_by_username_or_email.return_value = self.user
        mock_get_language_preference.return_value = self.lang_pref
        mock_get_membership_by_language.return_value = self.membership_by_lang_conf

        add_member_to_course_group_by_language(self.enrollment)

        mock_get_membership_by_language.assert_called_once_with(self.course_key)
        mock_get_user_by_username_or_email.assert_called_once_with(self.username)
        mock_get_language_preference.assert_called_once_with(self.user)
        mock_add_user_to_course_group.assert_called_once_with(
            self.user, self.membership_by_lang_conf[self.lang_pref], self.course_key
        )

    @patch(f"{HANDLERS_MODULE_PATH}.get_membership_by_language")
    @patch(f"{HANDLERS_MODULE_PATH}.get_user_by_username_or_email")
    @patch(f"{HANDLERS_MODULE_PATH}.get_language_preference")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_course_group")
    def test_add_member_to_course_group_by_language_no_group_for_lang(
        self,
        mock_add_user_to_course_group: Mock,
        mock_get_language_preference: Mock,
        mock_get_user_by_username_or_email: Mock,
        mock_get_membership_by_language: Mock,
    ):
        """Test `add_member_to_course_group_by_language` with no group for language"""
        self.lang_pref = "es"
        mock_get_user_by_username_or_email.return_value = self.user
        mock_get_language_preference.return_value = self.lang_pref
        mock_get_membership_by_language.return_value = self.membership_by_lang_conf

        add_member_to_course_group_by_language(self.enrollment)

        mock_get_membership_by_language.assert_called_once_with(self.course_key)
        mock_get_user_by_username_or_email.assert_called_once_with(self.username)
        mock_get_language_preference.assert_called_once_with(self.user)
        mock_add_user_to_course_group.assert_not_called()

    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_team")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort")
    def test_add_user_to_course_group_team_and_cohort(
        self,
        mock_add_user_to_cohort: Mock,
        mock_add_user_to_team: Mock,
    ):
        """Test `add_user_to_course_group` with team type"""
        course_groups = self.membership_by_lang_conf["en"]
        add_user_to_course_group(self.user, course_groups, self.course_key)

        mock_add_user_to_team.assert_called_once_with(self.user, self.team.id)
        mock_add_user_to_cohort.assert_called_once_with(
            self.user, self.cohort.id, self.course_key
        )

    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_team")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort")
    def test_add_user_to_course_group_team(
        self,
        mock_add_user_to_cohort: Mock,
        mock_add_user_to_team: Mock,
    ):
        """Test `add_user_to_course_group` with team type"""
        course_groups = [{"type": "team", "id": "team-id-1"}]
        add_user_to_course_group(self.user, course_groups, self.course_key)

        mock_add_user_to_team.assert_called_once_with(self.user, "team-id-1")
        mock_add_user_to_cohort.assert_not_called()

    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_team")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort")
    def test_add_user_to_course_group_cohort(
        self,
        mock_add_user_to_cohort: Mock,
        mock_add_user_to_team: Mock,
    ):
        """Test `add_user_to_course_group` with cohort type"""
        course_groups = [{"type": "cohort", "id": "cohort-name-1"}]
        add_user_to_course_group(self.user, course_groups, self.course_key)

        mock_add_user_to_cohort.assert_called_once_with(
            self.user, "cohort-name-1", self.course_key
        )
        mock_add_user_to_team.assert_not_called()

    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_team")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort")
    def test_add_user_to_course_group_no_type(
        self,
        mock_add_user_to_cohort: Mock,
        mock_add_user_to_team: Mock,
    ):
        """Test `add_user_to_course_group` with no type"""
        course_groups = [{"id": "group-id-1"}]
        add_user_to_course_group(self.user, course_groups, self.course_key)

        mock_add_user_to_cohort.assert_not_called()
        mock_add_user_to_team.assert_not_called()

    @patch(f"{HANDLERS_MODULE_PATH}.LANGUAGE_KEY", new=LANGUAGE_KEY)
    @patch(f"{HANDLERS_MODULE_PATH}.get_user_preference")
    def test_get_language_preference_with_preference(self, mock_get_user_pref: Mock):
        """Test `get_language_preference` when the user has a language preference"""
        mock_get_user_pref.return_value = "es-419"

        result = get_language_preference(self.user)

        mock_get_user_pref.assert_called_once_with(self.user, LANGUAGE_KEY)
        self.assertEqual(result, "es-419")

    @patch(f"{HANDLERS_MODULE_PATH}.LANGUAGE_KEY", new=LANGUAGE_KEY)
    @patch(f"{HANDLERS_MODULE_PATH}.get_user_preference")
    def test_get_language_preference_without_preference(self, mock_get_user_pref: Mock):
        """Test `get_language_preference` when the user does not have a language preference"""
        mock_get_user_pref.return_value = None

        result = get_language_preference(self.user)

        mock_get_user_pref.assert_called_once_with(self.user, LANGUAGE_KEY)
        self.assertEqual(result, "en")

    @patch(f"{HANDLERS_MODULE_PATH}.modulestore")
    def test_get_membership_by_language(self, mock_modulestore: Mock):
        """Test `get_membership_by_language` retrieves the correct settings"""
        mock_modulestore.return_value.get_course.return_value = self.course

        # MEMBERSHIP_BY_LANGUAGE_CONFIG setting exists
        result = get_membership_by_language(self.course_key)

        self.assertEqual(result, self.membership_by_lang_conf)
        mock_modulestore().get_course.assert_called_with(self.course_key)

        # MEMBERSHIP_BY_LANGUAGE_CONFIG setting has keys with comma-separated languages
        self.course.other_course_settings = {
            "MEMBERSHIP_BY_LANGUAGE_CONFIG": {
                "es-419,es-ES": self.membership_by_lang_conf["en"]
            }
        }
        expected_result = {
            "es-419": self.membership_by_lang_conf["en"],
            "es-es": self.membership_by_lang_conf["en"],
        }

        result = get_membership_by_language(self.course_key)

        self.assertEqual(len(result), 2)
        self.assertEqual(result, expected_result)
        mock_modulestore().get_course.assert_called_with(self.course_key)

        # MEMBERSHIP_BY_LANGUAGE_CONFIG does not exist
        self.course.other_course_settings = {}

        result = get_membership_by_language(self.course_key)

        self.assertEqual(result, {})
        mock_modulestore().get_course.assert_called_with(self.course_key)

    @patch(f"{HANDLERS_MODULE_PATH}.get_team_by_team_id")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_team_success(self, mock_log, mock_get_team_by_team_id):
        """Test `add_user_to_team` when the user is successfully added to the team."""
        mock_get_team_by_team_id.return_value = self.team

        add_user_to_team(self.user, self.team.id)

        mock_get_team_by_team_id.assert_called_once_with(self.team.id)
        self.team.add_user.assert_called_once_with(self.user)
        mock_log.info.assert_called_with(
            f"The user='{self.user}' has been added to the team='{self.team}'."
        )

    @patch(f"{HANDLERS_MODULE_PATH}.AlreadyOnTeamInTeamset", new=AlreadyOnTeamInTeamset)
    @patch(f"{HANDLERS_MODULE_PATH}.CourseTeamMembership")
    @patch(f"{HANDLERS_MODULE_PATH}.get_team_by_team_id")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_team_already_on_team(
        self,
        mock_log: Mock,
        mock_get_team_by_team_id: Mock,
        mock_course_team_membership: Mock,
    ):
        """Test `add_user_to_team` when the user is already on a team in the teamset."""
        self.team.add_user.side_effect = [AlreadyOnTeamInTeamset, None]
        mock_get_team_by_team_id.return_value = self.team
        old_membership = Mock(team="old-team")
        mock_course_team_membership.objects.filter().first.return_value = old_membership

        add_user_to_team(self.user, self.team.id)

        mock_get_team_by_team_id.assert_called_once_with(self.team.id)
        self.team.add_user.assert_called_with(self.user)
        self.assertEqual(self.team.add_user.call_count, 2)
        mock_log.debug.assert_called_with(
            f"The user='{self.user}' was moved from the "
            f"team='{old_membership.team}' to the team='{self.team}'."
        )

    @patch(
        f"{HANDLERS_MODULE_PATH}.NotEnrolledInCourseForTeam",
        new=NotEnrolledInCourseForTeam,
    )
    @patch(f"{HANDLERS_MODULE_PATH}.AlreadyOnTeamInTeamset", new=AlreadyOnTeamInTeamset)
    @patch(f"{HANDLERS_MODULE_PATH}.get_team_by_team_id")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_team_not_enrolled_in_course(
        self, mock_log: Mock, mock_get_team_by_team_id: Mock
    ):
        """Test `add_user_to_team` when the user is not enrolled in the course of the team."""
        self.team.add_user.side_effect = NotEnrolledInCourseForTeam
        mock_get_team_by_team_id.return_value = self.team

        add_user_to_team(self.user, self.team.id)

        mock_get_team_by_team_id.assert_called_once_with(self.team.id)
        self.team.add_user.assert_called_once_with(self.user)
        mock_log.exception.assert_called_with(
            f"The user='{self.user}' is not enrolled in the course of the team."
        )

    @patch(
        f"{HANDLERS_MODULE_PATH}.AddToIncompatibleTeamError",
        new=AddToIncompatibleTeamError,
    )
    @patch(
        f"{HANDLERS_MODULE_PATH}.NotEnrolledInCourseForTeam",
        new=NotEnrolledInCourseForTeam,
    )
    @patch(f"{HANDLERS_MODULE_PATH}.AlreadyOnTeamInTeamset", new=AlreadyOnTeamInTeamset)
    @patch(f"{HANDLERS_MODULE_PATH}.get_team_by_team_id")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_team_incompatible_team(
        self, mock_log: Mock, mock_get_team_by_team_id: Mock
    ):
        """Test `add_user_to_team` when the user cannot be added to the team."""
        self.team.add_user.side_effect = AddToIncompatibleTeamError
        mock_get_team_by_team_id.return_value = self.team

        add_user_to_team(self.user, self.team.id)

        mock_get_team_by_team_id.assert_called_once_with(self.team.id)
        self.team.add_user.assert_called_once_with(self.user)
        mock_log.exception.assert_called_with(
            f"The user='{self.user}' cannot be added to the team."
        )

    @patch(f"{HANDLERS_MODULE_PATH}.get_team_by_team_id")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_team_team_does_not_exist(
        self, mock_log, mock_get_team_by_team_id
    ):
        """Test `add_user_to_team` when the team does not exist."""
        mock_get_team_by_team_id.return_value = None
        self.team.add_user = Mock()

        add_user_to_team(self.user, self.team.id)

        mock_get_team_by_team_id.assert_called_once_with(self.team.id)
        mock_log.exception.assert_called_with(
            f"The team with the team_id='{self.team.id}' does not exist."
        )
        self.team.add_user.assert_not_called()

    @patch(f"{HANDLERS_MODULE_PATH}.get_cohort_by_name")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort_backend")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_cohort_success(
        self,
        mock_log: Mock,
        mock_add_user_to_cohort_backend: Mock,
        mock_get_cohort_by_name: Mock,
    ):
        """Test `add_user_to_cohort` when the operation is successful."""
        mock_get_cohort_by_name.return_value = self.cohort

        add_user_to_cohort(self.user, self.cohort.id, self.course_key)

        mock_get_cohort_by_name.assert_called_once_with(self.course_key, self.cohort.id)
        mock_add_user_to_cohort_backend.assert_called_once_with(self.cohort, self.user)
        mock_log.info.assert_called_once_with(
            f"The user='{self.user}' has been added to the cohort='{self.cohort}'."
        )

    @patch(f"{HANDLERS_MODULE_PATH}.CourseUserGroup")
    @patch(f"{HANDLERS_MODULE_PATH}.get_cohort_by_name")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_cohort_cohort_does_not_exist(
        self,
        mock_log: Mock,
        mock_get_cohort_by_name: Mock,
        mock_course_user_group: Mock,
    ):
        """Test `add_user_to_cohort` when the cohort does not exist."""
        mock_course_user_group.DoesNotExist = ObjectDoesNotExist
        mock_get_cohort_by_name.side_effect = ObjectDoesNotExist

        add_user_to_cohort(self.user, self.cohort.id, self.course_key)

        mock_get_cohort_by_name.assert_called_once_with(self.course_key, self.cohort.id)
        mock_log.exception.assert_called_once_with(
            f"The cohort with the cohort_name='{self.cohort.id}' does not exist."
        )

    @patch(f"{HANDLERS_MODULE_PATH}.CourseUserGroup")
    @patch(f"{HANDLERS_MODULE_PATH}.get_cohort_by_name")
    @patch(f"{HANDLERS_MODULE_PATH}.add_user_to_cohort_backend")
    @patch(f"{HANDLERS_MODULE_PATH}.log")
    def test_add_user_to_cohort_user_already_in_cohort(
        self,
        mock_log: Mock,
        mock_add_user_to_cohort_backend: Mock,
        mock_get_cohort_by_name: Mock,
        mock_course_user_group: Mock,
    ):
        """Test `add_user_to_cohort` when the user is already in the cohort."""
        mock_get_cohort_by_name.return_value = self.cohort
        mock_course_user_group.DoesNotExist = ObjectDoesNotExist
        mock_add_user_to_cohort_backend.side_effect = ValueError

        add_user_to_cohort(self.user, self.cohort.id, self.course_key)

        mock_get_cohort_by_name.assert_called_once_with(self.course_key, self.cohort.id)
        mock_add_user_to_cohort_backend.assert_called_once_with(self.cohort, self.user)
        mock_log.exception.assert_called_once_with(
            f"The user='{self.user}' is already in the cohort."
        )
