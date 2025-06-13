from domain.value_objects.project_management import ProjectCreateCommand, ProjectCreatePayload


def convert_project_create_command_to_payload(command: ProjectCreateCommand) -> ProjectCreatePayload:
    return ProjectCreatePayload(
        name=command.name,
        description=command.description,
        category_id=command.category_id,
        creator_id=command.creator_id,
        funding_model_id=command.funding_model_id,
        stage=command.stage,
        goal_sum=command.goal_sum,
        deadline=command.deadline.value,
        plan_file=command.plan_file,
    )
