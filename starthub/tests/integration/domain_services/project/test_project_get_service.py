from application.builders.domain_service.project_management import ProjectGetServiceBuilder
from django.test import TestCase
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.project_stage import ProjectStageEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.exceptions.permissions import ViewDeniedPermissionException
from domain.models.project_management.project import Project
from domain.services.permission import PermissionService
from domain.value_objects.common import Id, Slug
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.common import ProjectStageVo, ProjectStatus
from tests.common.builders import create_user_with_multiple_permissions, create_user_with_permission, get_random_user
from tests.common.check_raises import check_raises_in_docs


class TestProjectGetPermissionService(TestCase):
    def setUp(self):
        self.service = ProjectGetServiceBuilder.create_service()
        self.user_without_permission = get_random_user()

    def _create_user_with_view_any_project_status_permission(self, status: ProjectStatusEnum):
        """Helper to create user with VIEW.ANY permission for specific project status"""
        user, _, _ = create_user_with_permission(
            email=f"user_{status.value}@example.com",
            model=Project,
            action=ActionEnum.VIEW,
            scope=ScopeEnum.ANY,
            field=Project.STATUS_FIELD,
            value=status,
        )
        return user

    def _test_permission_check_positive(self, method, status: ProjectStatusEnum):
        """Helper for positive permission tests"""
        user = self._create_user_with_view_any_project_status_permission(status)
        method(user=user)

    def _test_permission_check_negative(self, method):
        """Helper for negative permission tests"""
        check_raises_in_docs(method, ViewDeniedPermissionException)
        with self.assertRaises(ViewDeniedPermissionException):
            method(user=self.user_without_permission)

    def test_check_can_user_read_submissions_with_permission(self):
        """Test user with proper permission can read submissions"""
        self._test_permission_check_positive(
            self.service.check_can_user_read_submissions, ProjectStatusEnum.UNDER_MODERATION
        )

    def test_check_can_user_read_submissions_without_permission(self):
        """Test user without permission cannot read submissions"""
        self._test_permission_check_negative(self.service.check_can_user_read_submissions)

    def test_check_can_user_read_rejected_with_permission(self):
        """Test user with proper permission can read rejected projects"""
        self._test_permission_check_positive(self.service.check_can_user_read_rejected, ProjectStatusEnum.REJECTED)

    def test_check_can_user_read_rejected_without_permission(self):
        """Test user without permission cannot read rejected projects"""
        self._test_permission_check_negative(self.service.check_can_user_read_rejected)

    def test_check_can_user_read_cancelled_with_permission(self):
        """Test user with proper permission can read cancelled projects"""
        self._test_permission_check_positive(self.service.check_can_user_read_cancelled, ProjectStatusEnum.CANCELLED)

    def test_check_can_user_read_cancelled_without_permission(self):
        """Test user without permission cannot read cancelled projects"""
        self._test_permission_check_negative(self.service.check_can_user_read_cancelled)

    def test_check_can_user_read_deactivated_with_permission(self):
        """Test user with proper permission can read deactivated projects"""
        self._test_permission_check_positive(
            self.service.check_can_user_read_deactivated, ProjectStatusEnum.DEACTIVATED
        )

    def test_check_can_user_read_deactivated_without_permission(self):
        """Test user without permission cannot read deactivated projects"""
        self._test_permission_check_negative(self.service.check_can_user_read_deactivated)


class TestProjectGetServicePrepareFilter(TestCase):
    def setUp(self):
        self.service = ProjectGetServiceBuilder.create_service()
        self.user_without_permissions = get_random_user()

        restricted_statuses = [
            ProjectStatusEnum.UNDER_MODERATION,
            ProjectStatusEnum.REJECTED,
            ProjectStatusEnum.CANCELLED,
            ProjectStatusEnum.DEACTIVATED,
        ]
        permissions = [
            PermissionService.create_permission_vo(
                model=Project, action=ActionEnum.VIEW, scope=ScopeEnum.ANY, field=Project.STATUS_FIELD, value=status
            )
            for status in restricted_statuses
        ]
        self.user_with_permissions, _, _ = create_user_with_multiple_permissions(
            email="can-view-any-project@example.com",
            role_name="admin",
            permission_names=[p.value for p in permissions],
        )

        self.accepted_statuses = [
            ProjectStatus(value=ProjectStatusEnum.ACTIVE),
            ProjectStatus(value=ProjectStatusEnum.COMPLETED),
            ProjectStatus(value=ProjectStatusEnum.DRAFT),
            ProjectStatus(value=ProjectStatusEnum.FUNDRAISING),
            ProjectStatus(value=ProjectStatusEnum.SUSPENDED),
        ]
        self.excluded_statuses = [ProjectStatus(value=s) for s in restricted_statuses]

    def _assert_denied(self, status, user):
        project_filter = ProjectFilter(statuses=[ProjectStatus(value=status)])
        with self.assertRaises(ViewDeniedPermissionException):
            self.service.prepare_filter_for_user(user, project_filter)

    def _assert_allowed(self, status):
        project_filter = ProjectFilter(statuses=[ProjectStatus(value=status)])
        prepared = self.service.prepare_filter_for_user(self.user_with_permissions, project_filter)
        expected = ProjectFilter(
            statuses=[ProjectStatus(value=status)],
            exclude_statuses=[i for i in self.excluded_statuses if i.value != status],
        )
        self.assertEqual(prepared, expected)

    def test_without_any_restricted_statuses(self):
        project_filter = ProjectFilter(
            id_=Id(value=1),
            id_list=[Id(value=1)],
            user_id=Id(value=1),
            category_slug=Slug(value="slug"),
            funding_model_slug=Slug(value="slug"),
            statuses=self.accepted_statuses,
            stage=ProjectStageVo(value=ProjectStageEnum.IDEA),
            exclude_statuses=None,
        )
        expected_filter = project_filter.model_copy()
        expected_filter.exclude_statuses = self.excluded_statuses

        prepared_filter = self.service.prepare_filter_for_user(
            user=self.user_without_permissions, filter_=project_filter
        )
        self.assertEqual(prepared_filter, expected_filter)

    def test_deny_to_view_with_restricted_statuses_for_ordinary_user(self):
        for status in [
            ProjectStatusEnum.UNDER_MODERATION,
            ProjectStatusEnum.DEACTIVATED,
            ProjectStatusEnum.CANCELLED,
            ProjectStatusEnum.REJECTED,
        ]:
            with self.subTest(status=status):
                self._assert_denied(status, user=self.user_without_permissions)

    def test_deny_to_view_with_restricted_statuses_for_not_user(self):
        for status in [
            ProjectStatusEnum.UNDER_MODERATION,
            ProjectStatusEnum.DEACTIVATED,
            ProjectStatusEnum.CANCELLED,
            ProjectStatusEnum.REJECTED,
        ]:
            with self.subTest(status=status):
                self._assert_denied(status, user=None)

    def test_user_with_permission_can_view_restricted_statuses(self):
        for status in [
            ProjectStatusEnum.UNDER_MODERATION,
            ProjectStatusEnum.REJECTED,
            ProjectStatusEnum.CANCELLED,
            ProjectStatusEnum.DEACTIVATED,
        ]:
            with self.subTest(status=status):
                self._assert_allowed(status)
