from typing import Any

from domain.value_objects.common import Description, Id
from domain.value_objects.company import CompanyName, CompanyUpdateCommand, EstablishedDate
from presentation.request_converters.common import build_address_create_command, parse_date
from rest_framework.request import Request


def _extract_established_date_or_none(data: dict[str, str]) -> EstablishedDate | None:
    established_date: EstablishedDate | None = None
    if "established_date" in data:
        established_date = EstablishedDate(value=parse_date(data["established_date"]))

    return established_date


def request_to_company_update_command(request: Request, company_id: int) -> CompanyUpdateCommand:
    """
    :raises DateIsNotIsoFormatException:
    :raises EmptyStringException:
    :raises CompanyNameIsTooLongException:
    :raises StringIsTooLongException: If the description is too long
    :raises DateIsNotIsoFormatException:
    :raises DateInFutureException:
    """

    data: dict[str, Any] = request.data

    return CompanyUpdateCommand(
        company_id=Id(value=company_id),
        name=CompanyName(value=data["name"]) if "name" in data else None,
        description=Description(value=data["description"]) if "description" in data else None,
        established_date=_extract_established_date_or_none(data=data),
        address_create_command=build_address_create_command(data["address"]) if "address" in data else None,
    )
