from datetime import date
from decimal import Decimal
from uuid import uuid4

from domain.enums.permission import ActionEnum, ScopeEnum
from domain.enums.project_status import ProjectStatusEnum
from domain.models import FundingModel, Project, ProjectCategory, ProjectStage
from domain.models.base import BaseModel
from domain.models.permission import Permission
from domain.models.role import Role
from domain.models.user_management.user import User
from domain.services.permission import PermissionService


def get_test_user():
    user, _ = User.objects.get_or_create(email="test@example.com", password="Password1234!")
    return user


def get_random_user():
    user, _ = User.objects.get_or_create(email=f"{uuid4().hex}@example.com", password="Password1234!")
    return user


def create_user_with_permission(
    email: str = "test@example.com",
    password: str = "Pass1234!",
    model: type[BaseModel] = None,
    action: ActionEnum = None,
    scope: ScopeEnum = None,
    field: str = None,
    value: str = None,
    permission_name: str = None,
) -> tuple[User, Role, Permission]:
    """
    Create regular user with role and permission for testing

    Args:
        email: User email
        password: User password
        model: Model for permission (if permission_name not provided)
        action: Action for permission (if permission_name not provided)
        scope: Scope for permission (if permission_name not provided)
        field: Field for permission (optional)
        value: Value for permission (optional)
        permission_name: Custom permission name (overrides other params)

    Returns:
        Tuple of (user, role, permission)
    """
    # Create permission name
    if permission_name:
        perm_name = permission_name
    elif model and action and scope:
        permission_vo = PermissionService.create_permission_vo(
            model=model, action=action, scope=scope, field=field, value=value
        )
        perm_name = permission_vo.value
    else:
        raise ValueError("Either permission_name or (model, action, scope) must be provided")

    permission, _ = Permission.objects.get_or_create(name=perm_name)

    # Create role and assign permission
    role, _ = Role.objects.get_or_create(name="user")
    role.permissions.add(permission)

    # Create user and assign role
    user, _ = User.objects.get_or_create(email=email, password=password)
    user.roles.add(role)

    return user, role, permission


def create_admin_with_permission(
    email: str = "admin@example.com",
    password: str = "Pass1234!",
    model: type[BaseModel] = None,
    action: ActionEnum = None,
    scope: ScopeEnum = None,
    field: str = None,
    value: str = None,
    permission_name: str = None,
) -> tuple[User, Role, Permission]:
    """
    Create admin user with role and permission for testing

    Args:
        email: Admin email
        password: Admin password
        model: Model for permission (if permission_name not provided)
        action: Action for permission (if permission_name not provided)
        scope: Scope for permission (if permission_name not provided)
        field: Field for permission (optional)
        value: Value for permission (optional)
        permission_name: Custom permission name (overrides other params)

    Returns:
        Tuple of (user, role, permission)
    """
    # Create permission name
    if permission_name:
        perm_name = permission_name
    elif model and action and scope:
        permission_vo = PermissionService.create_permission_vo(
            model=model, action=action, scope=scope, field=field, value=value
        )
        perm_name = permission_vo.value
    else:
        raise ValueError("Either permission_name or (model, action, scope) must be provided")

    permission, _ = Permission.objects.get_or_create(name=perm_name)

    # Create role and assign permission
    role, _ = Role.objects.get_or_create(name="admin")
    role.permissions.add(permission)

    # Create user and assign role
    user, _ = User.objects.get_or_create(email=email, password=password)
    user.roles.add(role)

    return user, role, permission


def create_user_with_multiple_permissions(
    email: str = "test@example.com",
    password: str = "Pass1234!",
    role_name: str = "admin",
    permission_names: list[str] = None,
) -> tuple[User, Role, list[Permission]]:
    """
    Create user with role and multiple permissions for testing

    Args:
        email: User email
        password: User password
        role_name: Role name
        permission_names: List of permission names

    Returns:
        Tuple of (user, role, list of permissions)
    """
    if not permission_names:
        permission_names = []

    # Create permissions
    permissions = []
    for perm_name in permission_names:
        permission, _ = Permission.objects.get_or_create(name=perm_name)
        permissions.append(permission)

    # Create role and assign permissions
    role, _ = Role.objects.get_or_create(name=role_name)
    role.permissions.set(permissions)

    # Create user and assign role
    user, _ = User.objects.get_or_create(email=email, password=password)
    user.roles.add(role)

    return user, role, permissions


def create_minimal_project(
    name="Test Project",
    description="Test project description",
    goal_sum=Decimal("100000.00"),
    deadline=date(2077, 12, 31),
    email="creator@example.com",
    password="Pass1234!",
    funding_model_name="Test Funding",
    stage_name="Idea Stage",
    category_name="Tech",
    status=ProjectStatusEnum.DRAFT.value,
) -> Project:
    user, _ = User.objects.get_or_create(email=email, defaults={"password": password})
    funding_model, _ = FundingModel.objects.get_or_create(name=funding_model_name)
    stage, _ = ProjectStage.objects.get_or_create(name=stage_name)
    category, _ = ProjectCategory.objects.get_or_create(name=category_name)

    project, created = Project.objects.get_or_create(
        name=name,
        defaults={
            "description": description,
            "creator": user,
            "funding_model": funding_model,
            "stage": stage,
            "status": status,
            "goal_sum": goal_sum,
            "deadline": deadline,
        },
    )

    if category not in project.categories.all():
        project.categories.add(category)

    return project
