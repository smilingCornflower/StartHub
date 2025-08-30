from datetime import date

from application.builders.app_service.project_management.project import ProjectUpdateAppServiceBuilder
from django.test import TestCase
from domain.enums.permission import ActionEnum, ScopeEnum
from domain.exceptions.project_management import ProjectCategoryNotFoundException
from domain.models import FundingModel
from domain.models.project_management.category import ProjectCategory
from domain.models.project_management.incubator import ProjectIncubator
from domain.models.project_management.project import Project
from domain.models.project_management.project_stage import ProjectStage
from domain.value_objects.common import DeadlineDate, Description, Id
from domain.value_objects.project.common import GoalSum, ProjectName
from domain.value_objects.project.funding_model import FundingModelId
from domain.value_objects.project.incubator import IncubatorName, IncubatorUpdatePayload
from domain.value_objects.project.metric import (
    Aov,
    Arppu,
    Arpu,
    Cac,
    ChurnRate,
    ConversionRate,
    Ltv,
    Nps,
    RetentionRate,
    Roi,
)
from domain.value_objects.project.project import ProjectUpdateCommand
from domain.value_objects.project.stage import ProjectStageId
from domain.value_objects.project.step import ProjectStepCreateCommand, ProjectStepDate, ProjectStepName
from tests.common.builders import create_minimal_project, create_user_with_permission


class TestProjectUpdateAppService(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user, _, _ = create_user_with_permission(
            email="test@example.com",
            model=Project,
            action=ActionEnum.CHANGE,
            scope=ScopeEnum.OWN,
        )
        cls.project = create_minimal_project(email=cls.user.email)
        cls.user_id = Id(value=cls.user.id)
        cls.project_id = Id(value=cls.project.id)

    def setUp(self):
        self.service = ProjectUpdateAppServiceBuilder.create_service()

    def _create_update_command(self, **kwargs):
        """Helper to create ProjectUpdateCommand with default project_id and user_id"""
        return ProjectUpdateCommand(project_id=self.project_id, user_id=self.user_id, **kwargs)

    def _get_updated_project(self):
        """Helper to get updated project from database"""
        return Project.objects.get(id=self.project_id.value)

    def test_update_project_name(self):
        """Test updating project name"""
        new_name = "Another Name"
        command = self._create_update_command(name=ProjectName(value=new_name))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().name, new_name)

    def test_update_project_description(self):
        """Test updating project description"""
        new_descr = "Another Description"
        command = self._create_update_command(description=Description(value=new_descr))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().description, new_descr)

    def test_update_project_goal_description(self):
        """Test updating project goal description"""
        new_goal_descr = "Another Goal Description"
        command = self._create_update_command(goal_description=Description(value=new_goal_descr))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().goal_description, new_goal_descr)

    def test_update_category_ids(self):
        """Test updating project categories"""
        new_category_1 = ProjectCategory.objects.create(name="New Category 1")
        new_category_2 = ProjectCategory.objects.create(name="New Category 2")
        command = self._create_update_command(category_ids=[Id(value=new_category_1.id), Id(value=new_category_2.id)])

        self.service.update(command)

        categories = list(self._get_updated_project().categories.all())
        self.assertEqual(categories, [new_category_1, new_category_2])

    def test_update_with_nonexisting_category_ids(self):
        """Test updating with non-existing category raises exception"""
        command = self._create_update_command(category_ids=[Id(value=-1)])

        with self.assertRaises(ProjectCategoryNotFoundException):
            self.service.update(command)

    def test_update_funding_model(self):
        """Test updating project funding model"""
        new_funding_model = FundingModel.objects.create(name="New Funding Model")
        command = self._create_update_command(funding_model_id=FundingModelId(value=new_funding_model.id))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().funding_model, new_funding_model)

    def test_update_project_stage(self):
        """Test updating project stage"""
        new_stage = ProjectStage.objects.create(name="New Stage")
        command = self._create_update_command(stage_id=ProjectStageId(value=new_stage.id))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().stage, new_stage)

    def test_update_goal_sum(self):
        """Test updating project goal sum"""
        new_goal_sum = 145_000
        command = self._create_update_command(goal_sum=GoalSum(value=new_goal_sum))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().goal_sum, new_goal_sum)

    def test_update_deadline_date(self):
        """Test updating project deadline"""
        new_deadline = date(2088, 11, 28)
        command = self._create_update_command(deadline=DeadlineDate(value=new_deadline))

        self.service.update(command)

        self.assertEqual(self._get_updated_project().deadline, new_deadline)

    def test_update_steps(self):
        """Test updating project steps"""
        new_steps = [
            ProjectStepCreateCommand(
                name=ProjectStepName(value="Another Name"),
                description=Description(value="Another Description"),
                date=ProjectStepDate(value=date(2099, 10, 20)),
            )
        ]
        command = self._create_update_command(steps=new_steps)

        self.service.update(command)

        updated_step = self._get_updated_project().steps.all().first()
        new_step = new_steps[0]
        self.assertEqual(updated_step.name, new_step.name.value)
        self.assertEqual(updated_step.description, new_step.description.value)
        self.assertEqual(updated_step.date, new_step.date.value)

    def test_update_incubator_when_project_doesnt_have_incubator(self):
        """Test creating incubator when project doesn't have one"""
        new_incubator = IncubatorUpdatePayload(
            project_id=self.project_id,
            name=IncubatorName(value="New Incubator"),
            description=Description(value="New Description"),
        )
        command = self._create_update_command(incubator=new_incubator)

        self.service.update(command)

        updated_incubator = self._get_updated_project().incubator
        self.assertEqual(updated_incubator.project_id, new_incubator.project_id.value)
        self.assertEqual(updated_incubator.name, new_incubator.name.value)
        self.assertEqual(updated_incubator.description, new_incubator.description.value)

    def test_update_incubator_when_project_have_incubator(self):
        """Test updating existing incubator"""
        ProjectIncubator.objects.create(project_id=self.project_id, name="Name", description="Description")

        another_incubator = IncubatorUpdatePayload(
            project_id=self.project_id,
            name=IncubatorName(value="Another Incubator"),
            description=Description(value="Another Description"),
        )
        command = self._create_update_command(incubator=another_incubator)

        self.service.update(command)

        updated_incubator = self._get_updated_project().incubator
        self.assertEqual(updated_incubator.project_id, another_incubator.project_id.value)
        self.assertEqual(updated_incubator.name, another_incubator.name.value)
        self.assertEqual(updated_incubator.description, another_incubator.description.value)

    def test_update_metrics(self):
        """Test updating all project metrics"""
        command = self._create_update_command(
            ltv=Ltv(value=1000.5),
            arpu=Arpu(value=50.25),
            arppu=Arppu(value=75.3),
            cac=Cac(value=100.0),
            nps=Nps(value=8.5),
            roi=Roi(value=15.5),
            aov=Aov(value=120.0),
            churn_rate=ChurnRate(value=5.2),
            retention_rate=RetentionRate(value=85.7),
            conversion_rate=ConversionRate(value=3.4),
        )

        self.service.update(command)

        project = self._get_updated_project()
        self.assertEqual(project.ltv, command.ltv.value)
        self.assertEqual(project.arpu, command.arpu.value)
        self.assertEqual(project.arppu, command.arppu.value)
        self.assertEqual(project.cac, command.cac.value)
        self.assertEqual(project.nps, command.nps.value)
        self.assertEqual(project.roi, command.roi.value)
        self.assertEqual(project.aov, command.aov.value)
        self.assertEqual(project.churn_rate, command.churn_rate.value)
        self.assertEqual(project.retention_rate, command.retention_rate.value)
        self.assertEqual(project.conversion_rate, command.conversion_rate.value)
