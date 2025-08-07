from dataclasses import asdict
from json.decoder import JSONDecodeError
from pprint import pformat

import pydantic
from application.converters.request_converters.search import request_data_to_project_search_params
from application.dto.auth import AccessPayloadDto, AnonymousPayloadDto
from application.dto.project import ProjectDto
from application.services.gateway import gateway
from domain.enums.token import TokenTypeEnum
from domain.exceptions import CustomException
from domain.exceptions.project_management import ProjectNotFoundException
from domain.models.project_management.project import Project
from domain.value_objects.common import Id, OffsetPagination, Pagination
from domain.value_objects.filter import ProjectFilter
from domain.value_objects.project.image import (
    ProjectImageCreateCommand,
    ProjectImageDeleteCommand,
    ProjectImageUpdateCommand,
)
from domain.value_objects.project.project import ProjectCreateCommand, ProjectUpdateCommand
from domain.value_objects.search import ProjectSearchParams
from infrastructure.auth.token import get_access_or_anonymous_payload_dto_from_headers
from infrastructure.auth.user import get_user_id_or_none, get_user_id_or_raises
from loguru import logger
from presentation.constants import SUCCESS
from presentation.request_converters.common import request_to_offset_pagination, request_to_pagination
from presentation.request_converters.project.request_files_to_project_image_create_command import (
    request_files_to_project_image_create_command,
)
from presentation.request_converters.project.request_to_project_create_command import request_to_project_create_command
from presentation.request_converters.project.request_to_project_filter import request_to_project_filter
from presentation.request_converters.project.request_to_project_images_update_command import (
    request_project_data_to_project_images_update_command,
)
from presentation.request_converters.project.request_to_project_update_command import (
    request_to_the_project_update_command,
)
from presentation.response_factories.common import ProjectErrorResponseFactory
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ProjectView(APIView):
    parser_classes = [MultiPartParser]

    @staticmethod
    def get(request: Request, project_id: int | None = None) -> Response:
        print()
        logger.info("GET project request", project_id=project_id, query_params=request.query_params)
        try:
            user_id: Id | None = get_user_id_or_none(request=request)

            if project_id is not None:
                project: ProjectDto = gateway.project_get_app_service.get_by_id(
                    project_id=Id(value=project_id),
                    user_id=user_id if user_id else None,
                )
                return Response(asdict(project), status=status.HTTP_200_OK)

            else:
                pagination: Pagination = request_to_pagination(request=request)
                project_filter: ProjectFilter = request_to_project_filter(request=request)

                logger.debug(f"pagination = {pagination}")
                logger.debug(f"project_filter: \n{pformat(project_filter.__dict__)}")

                projects: list[ProjectDto] = gateway.project_get_app_service.get(
                    filter_=project_filter,
                    pagination=pagination,
                    user_id=user_id,
                )
        except CustomException as e:
            return ProjectErrorResponseFactory.create_response(e)
        return Response(map(asdict, projects), status=status.HTTP_200_OK)

    @staticmethod
    def post(request: Request) -> Response:
        print()
        logger.warning("POST /projects/")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectCreateCommand = request_to_project_create_command(request=request, user_id=int(user_id))

            project: Project = gateway.project_create_app_service.create(command=command)
        except (CustomException, pydantic.ValidationError, JSONDecodeError) as e:
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"project_id": project.id, "code": "SUCCESS"}, status=status.HTTP_201_CREATED)

    @staticmethod
    def patch(request: Request, project_id: int) -> Response:
        print()
        logger.info(f"PATCH /projects/{project_id}/")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command: ProjectUpdateCommand = request_to_the_project_update_command(
                request=request, project_id=project_id, user_id=int(user_id)
            )
            logger.debug(f"command: \n {pformat(command.__dict__)}")

            gateway.project_update_app_service.update(command=command)
            return Response({"detail": "updated successfully.", "code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError, JSONDecodeError) as e:
            return ProjectErrorResponseFactory.create_response(e)

    @staticmethod
    def delete(request: Request, project_id: int) -> Response:
        print()
        logger.info(f"DELETE /projects/{project_id}/")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            project_delete_service = gateway.project_delete_app_service
            project_delete_service.delete(project_id=Id(value=project_id), user_id=user_id)

            return Response({"code": SUCCESS}, status=status.HTTP_200_OK)

        except (CustomException, pydantic.ValidationError) as e:
            return ProjectErrorResponseFactory.create_response(e)


class MeProjectView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        logger.info(f"GET /my/projects/ request.query_params: {request.query_params}")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            pagination: Pagination = request_to_pagination(request=request)

            projects: list[ProjectDto] = gateway.project_get_app_service.get(
                filter_=ProjectFilter(user_id=user_id), pagination=pagination, user_id=user_id
            )
            return Response(map(asdict, projects), status=status.HTTP_200_OK)
        except CustomException as e:
            return ProjectErrorResponseFactory.create_response(e)


class ProjectPlanView(APIView):
    parser_classes = [MultiPartParser]
    error_classes: tuple[type[Exception], ...] = tuple(ProjectErrorResponseFactory.error_codes.keys())

    @staticmethod
    def get(request: Request, project_id: int) -> Response:
        try:
            plan_url: str = gateway.project_get_app_service.get_plan_url(project_id=Id(value=project_id))
            return Response({"plan_url": plan_url, "code": SUCCESS}, status=status.HTTP_200_OK)
        except ProjectNotFoundException:
            return Response({"detail": f"Project with id = {project_id} not found."}, status=status.HTTP_404_NOT_FOUND)


class ProjectImageView(APIView):
    error_classes: tuple[type[Exception], ...] = tuple(ProjectErrorResponseFactory.error_codes.keys())

    def post(self, request: Request, project_id: int) -> Response:
        logger.info(f"POST project photo request.\n\t {project_id=}")

        try:
            user_id: int = get_user_id_or_raises(request=request).value
            image_create_command: ProjectImageCreateCommand = request_files_to_project_image_create_command(
                files=request.FILES, project_id=project_id, user_id=user_id
            )
            gateway.project_image_app_service.create(image_create_command=image_create_command)
        except self.error_classes as e:
            logger.exception(f"Exception: {repr(e)}")
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"detail": "Image uploaded successfully.", "code": SUCCESS}, status=status.HTTP_201_CREATED)

    def get(self, request: Request, project_id: int) -> Response:
        logger.info(f"GET project photo request.\n\t {project_id=}")

        try:
            image_urls: list[str] = gateway.project_image_app_service.get_image_urls(project_id=Id(value=project_id))
            return Response(image_urls, status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.exception(f"Exception: {repr(e)}")
            return ProjectErrorResponseFactory.create_response(e)

    def delete(self, request: Request, project_id: int, image_order: int) -> Response:
        logger.info(f"GET /projects/images/ \n\t {project_id=}\n\t {image_order=}")

        try:
            user_id: Id = get_user_id_or_raises(request=request)
            command = ProjectImageDeleteCommand(
                project_id=Id(value=project_id), image_order=image_order, user_id=user_id
            )
            gateway.project_image_app_service.delete_image(command=command)
            return Response({"detail": "image deleted successfully", "code": SUCCESS}, status=status.HTTP_200_OK)
        except self.error_classes as e:
            logger.exception(f"Exception: {repr(e)}")
            return ProjectErrorResponseFactory.create_response(e)

    def patch(self, request: Request, project_id: int) -> Response:
        logger.info(f"PATCH /projects/images/ \n\t {request.data=}")
        try:
            user_id: Id = get_user_id_or_raises(request=request)
            image_update_command: ProjectImageUpdateCommand = request_project_data_to_project_images_update_command(
                data=request.data, project_id=project_id, user_id=user_id.value
            )
            gateway.project_image_app_service.update_project_images(command=image_update_command)
        except self.error_classes as e:
            logger.exception(f"Exception: {repr(e)}")
            return ProjectErrorResponseFactory.create_response(e)

        return Response({"detail": "image deleted successfully", "code": SUCCESS}, status=status.HTTP_200_OK)


class ProjectSearchView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print()
        logger.info("GET /project/search/")
        logger.debug(f"query_params = {request.query_params}")
        try:
            # TODO: Write method get_user_id() instead of get_token()
            token: AccessPayloadDto | AnonymousPayloadDto = get_access_or_anonymous_payload_dto_from_headers(
                headers=request.headers
            )
            logger.info(f"Received token type = {type(token)}")
            user_id: Id | None = None
            if token.type == TokenTypeEnum.ACCESS:
                user_id = Id(value=int(token.sub))

            search_params: ProjectSearchParams = request_data_to_project_search_params(query=request.query_params)
            offset_pagination: OffsetPagination = request_to_offset_pagination(query_params=request.query_params)
            logger.debug(f"search_params = {search_params}")
            logger.debug(f"offset_pagination = {offset_pagination}")

            projects: list[ProjectDto] = gateway.project_get_app_service.search(
                search_params=search_params, offset_pagination=offset_pagination, user_id=user_id
            )
            return Response(map(asdict, projects), status=status.HTTP_200_OK)

        except CustomException as e:
            return ProjectErrorResponseFactory.create_response(e)
