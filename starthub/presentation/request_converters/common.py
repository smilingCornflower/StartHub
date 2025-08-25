from datetime import date
from typing import cast

from django.http import QueryDict
from domain.enums.language import LangCodeEnum
from domain.enums.role import RoleEnum
from domain.exceptions.validation import DateIsNotIsoFormatException, MissingRequiredFieldException, ValidationException
from domain.value_objects.common import OffsetPagination, Pagination
from domain.value_objects.country import CountryCode
from domain.value_objects.geo import AddressCreateCommand, CityId, RegionId
from loguru import logger
from rest_framework.request import Request


def request_to_pagination(request: Request) -> Pagination:
    query_params = request.query_params
    return Pagination(
        last_id=int(cast(str, query_params.get("last_id"))) if "last_id" in query_params else None,
        limit=int(get_required_field(query_params, "limit")),
    )


def request_to_offset_pagination(query_params: QueryDict) -> OffsetPagination:
    return OffsetPagination(
        offset=int(cast(str, query_params["offset"])) if "offset" in query_params else 0,
        limit=int(get_required_field(query_params, "limit")),
    )


def get_required_field[T](data: dict[str, T], field: str, field_name_in_exception: str | None = None) -> T:
    """:raises MissingRequiredFieldException:"""
    if field_name_in_exception is None:
        field_name_in_exception = field
    if field not in data:
        logger.exception(f"Missing required field: {field_name_in_exception}.")
        raise MissingRequiredFieldException(f"Missing required field: {field_name_in_exception}.")
    return data[field]


def parse_date(date_str: str) -> date:
    """:raises DateIsNotIsoFormatException:"""
    try:
        return date.fromisoformat(date_str)
    except ValueError as e:
        logger.exception(f"Exception during parsing established_date: {repr(e)}.")
        raise DateIsNotIsoFormatException("Date must be in iso format.") from e


def build_address_create_command(address_data: dict[str, str]) -> AddressCreateCommand:
    """Build AddressVo from address data."""
    return AddressCreateCommand(
        country_code=CountryCode(value=get_required_field(address_data, "country_code", "address.country_code")),
        region_id=RegionId(value=int(get_required_field(address_data, "region_id"))),
        city_id=CityId(value=int(get_required_field(address_data, "city_id"))),
        district=address_data.get("district"),
        street=address_data.get("street"),
        house_number=address_data.get("house_number"),
        postal_code=address_data.get("postal_code"),
        raw_address=address_data.get("raw_address"),
    )


def parse_languages(request: Request) -> list[LangCodeEnum]:
    lang_param: str | None = request.query_params.get("lang")
    if lang_param:
        print(1)
        languages = lang_param.split(",")
        language_codes: list[LangCodeEnum] = list()
        for lang in languages:
            try:
                language_codes.append(LangCodeEnum(lang))
            except ValueError:
                logger.debug(f"Unsupported lang='{lang}'.")
        return language_codes
    else:
        return [LangCodeEnum.get_default()]


def get_role_if_exists_from_params(params: QueryDict) -> RoleEnum | None:
    """:raises ValidationException:"""
    if params.get("role"):
        try:
            return RoleEnum(value=cast(str, params["role"]))
        except ValueError:
            allowed = ", ".join([item for item in RoleEnum])
            raise ValidationException(f"Invalid value for role: {params['role']}. Expected: {allowed}")
    else:
        return None
