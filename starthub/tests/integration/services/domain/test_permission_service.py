from application.service_factories.domain_service.permission import PermissionServiceFactory
from django.test import TestCase
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.models import Project
from domain.models.permission import Permission
from domain.models.role import Role
from domain.models.user import User
from domain.value_objects.common import Id
from domain.value_objects.user import PermissionVo
from loguru import logger


class TestPermissionService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.service = PermissionServiceFactory.create_service()
        logger.info(f"all_roles: {Role.objects.all()}")
        logger.info(f"all_permissions: {Permission.objects.all()}")
        cls.blogger = User.objects.create_user(
            first_name="name", last_name="surname", email="test@email.com", password="ValidPass1234"
        )
        cls.blogger_role = Role.objects.get(name="blogger")
        cls.blogger.roles.add(cls.blogger_role)

    def test_valid_permission_create(self):
        permission_1 = self.service.create_permission_vo(Project, ActionEnum.CHANGE, ScopeEnum.ANY)
        permission_2 = self.service.create_permission_vo(Project, ActionEnum.CHANGE, ScopeEnum.ANY, field="description")
        permission_3 = self.service.create_permission_vo(Project, "change", "any", field="description")

        self.assertTrue(permission_1, PermissionVo(value="change.any.project"))
        self.assertTrue(permission_2, PermissionVo(value="change.any.project.description"))
        self.assertTrue(permission_3, PermissionVo(value="change.any.project.description"))

    def test_invalid_model_permission_create(self):
        with self.assertRaises(TypeError):
            self.service.create_permission_vo(ActionEnum, ActionEnum.CHANGE, ScopeEnum.ANY)

    def test_invalid_action_permission_create(self):
        with self.assertRaises(ValueError):
            self.service.create_permission_vo(Project, "invalid_action", ScopeEnum.ANY)

    def test_invalid_scope_permission_create(self):
        with self.assertRaises(ValueError):
            self.service.create_permission_vo(Project, ActionEnum, "all")

    def test_blogger_has_existing_permission(self):
        for i in ["add.any.news", "change.any.news", "delete.any.news"]:
            with self.subTest(action=i):
                permission = PermissionVo(value=i)
                result = self.service.has_permission(user_id=Id(value=self.blogger.id), permission_vo=permission)
                self.assertTrue(result)

    def test_not_existing_permission(self):
        permission = PermissionVo(value="add.any.another_model")
        result = self.service.has_permission(user_id=Id(value=self.blogger.id), permission_vo=permission)
        self.assertFalse(result)
