from application.builders.domain_service.permission import PermissionServiceBuilder
from django.test import TestCase
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.models.permission import Permission
from domain.models.role import Role
from domain.models.user_management.user import User
from domain.value_objects.common import Id
from domain.value_objects.user_management.user import PermissionVo


class TestPermissionService(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Test data
        cls.model = User
        cls.action = ActionEnum.CHANGE
        cls.scope = ScopeEnum.ANY
        cls.field = User.IS_ACTIVE_FIELD
        cls.value = True

        # Database setup
        cls.email = "test@example.com"
        cls.password = "Pass1234!"
        cls.role_name = "admin"

        permission_name = f"{cls.action}.{cls.scope}.{cls.model.get_permission_key()}"
        cls.permission, _ = Permission.objects.get_or_create(name=permission_name)
        cls.role, _ = Role.objects.get_or_create(name=cls.role_name)
        cls.role.permissions.add(cls.permission)

        cls.user, _ = User.objects.get_or_create(email=cls.email, password=cls.password)
        cls.user.roles.add(cls.role)

    def setUp(self):
        self.service = PermissionServiceBuilder.create_service()

    def test_create_permission_vo_basic(self):
        """Test basic permission creation without field and value"""
        permission = self.service.create_permission_vo(model=self.model, action=self.action, scope=self.scope)
        expected = f"{self.action}.{self.scope}.{self.model.get_permission_key()}"
        self.assertEqual(permission.value, expected)

    def test_create_permission_vo_with_field(self):
        """Test permission creation with field"""
        permission = self.service.create_permission_vo(
            model=self.model, action=self.action, scope=self.scope, field=self.field
        )
        expected = f"{self.action}.{self.scope}.{self.model.get_permission_key()}.{self.field}"
        self.assertEqual(permission.value, expected)

    def test_create_permission_vo_with_field_and_value(self):
        """Test permission creation with field and value"""
        permission = self.service.create_permission_vo(
            model=self.model, action=self.action, scope=self.scope, field=self.field, value=self.value
        )
        expected = f"{self.action}.{self.scope}.{self.model.get_permission_key()}.{self.field}.{self.value}"
        self.assertEqual(permission.value, expected)

    def test_invalid_model_type_raises_type_error(self):
        """Must throw exception if model doesn't inherit from BaseModel"""

        class DummyModel:
            def get_permission_key(self):
                return "dummy_model"

        with self.assertRaises(TypeError):
            self.service.create_permission_vo(model=DummyModel, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY)

    def test_invalid_field_raises_value_error(self):
        """Must throw exception if model hasn't the field"""
        with self.assertRaises(ValueError):
            self.service.create_permission_vo(
                model=User, action=ActionEnum.CHANGE, scope=ScopeEnum.ANY, field="non_existing_field"
            )

    def test_has_permission_with_existing_permission(self):
        """Test user has permission when permission exists"""
        permission_vo = self.service.create_permission_vo(model=self.model, action=self.action, scope=self.scope)
        has_permission = self.service.has_permission(user_id=Id(value=self.user.id), permission_vo=permission_vo)
        self.assertTrue(has_permission)

    def test_has_permission_without_permission(self):
        """Test user doesn't have permission when permission doesn't exist"""
        permission_vo = PermissionVo(value="view.any.another_model")
        has_permission = self.service.has_permission(user_id=Id(value=self.user.id), permission_vo=permission_vo)
        self.assertFalse(has_permission)

    def test_is_allowed_for_user_with_permission(self):
        """Test user is allowed when has permission"""
        is_allowed = self.service.is_allowed_for_user(
            user=self.user, model=self.model, action=self.action, scope=self.scope
        )
        self.assertTrue(is_allowed)

    def test_is_allowed_for_user_without_permission(self):
        """Test user is not allowed when doesn't have permission"""
        is_allowed = self.service.is_allowed_for_user(
            user=self.user, model=self.model, action=ActionEnum.VIEW, scope=ScopeEnum.OWN
        )
        self.assertFalse(is_allowed)

    def test_has_user_permission_with_permission(self):
        """Test has_user_permission returns True when user has permission"""
        permission_vo = self.service.create_permission_vo(model=self.model, action=self.action, scope=self.scope)
        has_permission = self.service.has_user_permission(user=self.user, permission_vo=permission_vo)
        self.assertTrue(has_permission)

    def test_has_user_permission_without_permission(self):
        """Test has_user_permission returns False when user doesn't have permission"""
        permission_vo = PermissionVo(value="delete.own.another_model")
        has_permission = self.service.has_user_permission(user=self.user, permission_vo=permission_vo)
        self.assertFalse(has_permission)
