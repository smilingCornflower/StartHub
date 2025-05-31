from dataclasses import asdict

from application.dto.project import ProjectDto
from application.service_factories.project import ProjectServiceFactory
from application.services.project import ProjectAppService
from application.utils.get_access_payload_dto import get_access_payload_dto
from domain.exceptions.auth import InvalidTokenException
from domain.exceptions.project import ProjectNotFoundException
from domain.exceptions.validation import ValidationException
from domain.models.project import Project
from loguru import logger
from presentation.response_factories.common import ProjectErrorResponseFactory
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectView(APIView):
    parser_classes = [JSONParser]  # application/json
    error_classes: tuple[type[Exception], ...] = tuple(ProjectErrorResponseFactory.error_codes.keys())

    @staticmethod
    def get(request: Request, project_id: int | None = None) -> Response:
        logger.info(f"request_data = {request.query_params}; project_id = {project_id}")
        project_service: ProjectAppService = ProjectServiceFactory.create_service()

        if project_id:
            try:
                project: ProjectDto = project_service.get_by_id(project_id=project_id)
                return Response(asdict(project), status=status.HTTP_200_OK)
            except ProjectNotFoundException:
                return Response(
                    {"detail": f"Project with id = {project_id} not found."}, status=status.HTTP_404_NOT_FOUND
                )

        projects: list[ProjectDto] = project_service.get(request.query_params)
        return Response(map(asdict, projects), status=status.HTTP_200_OK)

    def post(self, reqeust: Request) -> Response:
        try:
            access_dto = get_access_payload_dto(reqeust.COOKIES)
        except (ValidationException, InvalidTokenException) as e:
            return Response({"detail": str(e), "code": "UNAUTHORIZED"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            project_service: ProjectAppService = ProjectServiceFactory.create_service()
            project: Project = project_service.create(data=reqeust.data, user_id=int(access_dto.sub))
        except self.error_classes as e:
            # error: Exception type must be derived from BaseException (or be a tuple of exception classes)  [misc]
            logger.error(f"Exception: {e}")
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"project_id": project.id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)

    def patch(self, request: Request, project_id: int) -> Response:
        try:
            access_dto = get_access_payload_dto(request.COOKIES)
        except (ValidationException, InvalidTokenException) as e:
            return Response({"detail": str(e), "code": "UNAUTHORIZED"}, status=status.HTTP_400_BAD_REQUEST)

        project_service: ProjectAppService = ProjectServiceFactory.create_service()
        logger.debug("Project service created.")
        try:
            project_service.update(request.data, project_id=project_id, user_id=int(access_dto.sub))
        except self.error_classes as e:
            logger.error(f"Exception: {e}")
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"detail": "updated successfully.", "code": "SUCCESS"}, 200)

    def delete(self, request: Request, project_id: int) -> Response:
        try:
            access_dto = get_access_payload_dto(request.COOKIES)
        except (ValidationException, InvalidTokenException) as e:
            return Response({"detail": str(e), "code": "UNAUTHORIZED"}, status=status.HTTP_400_BAD_REQUEST)

        project_service: ProjectAppService = ProjectServiceFactory.create_service()
        logger.debug("Project service created.")
        try:
            project_service.delete(project_id, int(access_dto.sub))
        except self.error_classes as e:
            logger.error(f"Exception: {e}")
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"detail": "deleted successfully.", "code": "SUCCESS"}, 200)
