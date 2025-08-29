from django.test import SimpleTestCase
from domain.exceptions.project_management import NegativeProjectGoalSumException
from domain.value_objects.project.common import GoalSum
from tests.utils import check_raises


class TestData:
    VALID_GOAL = 1000
    ZERO_GOAL = 0
    NEGATIVE_GOAL = -500


class TestGoalSum(SimpleTestCase):
    def test_valid_goal(self):
        obj = GoalSum(value=TestData.VALID_GOAL)
        self.assertEqual(obj.value, TestData.VALID_GOAL)

    def test_zero_goal_raises_exception(self):
        exc = NegativeProjectGoalSumException
        check_raises(GoalSum.is_positive_goal_sum, exc)
        with self.assertRaises(exc):
            GoalSum(value=TestData.ZERO_GOAL)

    def test_negative_goal_raises_exception(self):
        exc = NegativeProjectGoalSumException
        check_raises(GoalSum.is_positive_goal_sum, exc)
        with self.assertRaises(exc):
            GoalSum(value=TestData.NEGATIVE_GOAL)
