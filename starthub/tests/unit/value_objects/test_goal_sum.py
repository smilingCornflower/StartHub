from django.test import SimpleTestCase
from domain.exceptions.project_management import NegativeProjectGoalSumException
from domain.value_objects.project_management import GoalSum


class TestGoalSum(SimpleTestCase):
    def check_raises(self, exc, func):
        self.assertTrue(f":raises {exc.__name__}:" in func.__doc__, "raises not in docstring.")

    def test_valid_sum(self):
        goal_sum = GoalSum(value=1000)
        self.assertEqual(goal_sum.value, 1000)

    def test_negative_sum(self):
        with self.assertRaises(NegativeProjectGoalSumException):
            GoalSum(value=-100)
        self.check_raises(NegativeProjectGoalSumException, GoalSum.is_positive_goal_sum)
