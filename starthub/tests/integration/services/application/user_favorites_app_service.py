from application.dto.project import ProjectDto
from application.dto.user import UserFavoriteDto
from application.service_factories.app_service.user_favorite import UserFavoriteAppAppServiceBuilder
from application.services.user_management.user_favorite import UserFavoriteAppService
from django.test import TestCase
from domain.exceptions.project_management import ProjectNotFoundException
from domain.exceptions.user import UserNotFoundException
from domain.exceptions.user_favorite import UserFavoriteAlreadyExistsException, UserFavoriteNotFoundException
from domain.models.project_management.project import Project
from domain.models.user_management.user import User
from domain.models.user_management.user_favorite import UserFavorite
from domain.value_objects.common import Id
from tests.factories.project import create_project_instance
from tests.utils import check_raises


class TestUserFavoritesAppService(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(email="test@example.com", password="ValidPass1234")
        project: Project = create_project_instance(user_id=Id(value=user.id))

        cls.user_id = user.id
        cls.project_id = project.id

    def setUp(self):
        self.service: UserFavoriteAppService = UserFavoriteAppAppServiceBuilder.create_service()

    def test_add_favorite(self):
        self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)
        user_favorites: list[UserFavorite] = list(UserFavorite.objects.filter(user_id=self.user_id).all())
        self.assertEqual(user_favorites[0].project_id, self.project_id)

    def test_get_user_favorite_projects(self):
        self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)
        projects: list[ProjectDto] = self.service.get_user_favorite_projects(user_id=self.user_id)
        self.assertEqual(len(projects), 1)
        self.assertIsInstance(projects[0], ProjectDto)

    def test_delete_by_association_ids(self):
        self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)
        self.service.delete_by_association_ids(user_id=self.user_id, project_id=self.project_id)

        with self.assertRaises(UserFavorite.DoesNotExist):
            UserFavorite.objects.get(user_id=self.user_id, project_id=self.project_id)

    def test_add_favorite_with_not_existing_user(self):
        with self.assertRaises(UserNotFoundException):
            self.service.add_favorite(user_id=-1, project_id=self.project_id)
        check_raises(func=self.service.add_favorite, exc=UserNotFoundException)

    def test_add_favorite_with_not_existing_project(self):
        with self.assertRaises(ProjectNotFoundException):
            self.service.add_favorite(user_id=self.user_id, project_id=-1)
        check_raises(func=self.service.add_favorite, exc=ProjectNotFoundException)

    def test_add_favorite_with_already_existing_favorite(self):
        self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)

        with self.assertRaises(UserFavoriteAlreadyExistsException):
            self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)
        check_raises(func=self.service.add_favorite, exc=UserFavoriteAlreadyExistsException)

    def test_get_favorites_projects_for_not_existing_user(self):
        with self.assertRaises(UserNotFoundException):
            self.service.get_user_favorite_projects(user_id=-1)
        check_raises(func=self.service.get_user_favorite_projects, exc=UserNotFoundException)

    def test_delete_not_existing_user_favorite(self):
        with self.assertRaises(UserFavoriteNotFoundException):
            self.service.delete_by_association_ids(user_id=-1, project_id=-1)
        check_raises(func=self.service.delete_by_association_ids, exc=UserFavoriteNotFoundException)

    def test_get_user_favorites(self):
        self.service.add_favorite(user_id=self.user_id, project_id=self.project_id)

        user_favorites: list[UserFavoriteDto] = self.service.get_user_favorites(self.user_id)
        self.assertEqual(len(user_favorites), 1)
        self.assertIsInstance(user_favorites[0], UserFavoriteDto)
