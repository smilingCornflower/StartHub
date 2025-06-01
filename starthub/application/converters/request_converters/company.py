from typing import Any

from application.draft.company import CompanyCreateDraft
from domain.value_objects.common import Id
from domain.value_objects.company import BusinessNumber
from domain.value_objects.country import CountryCode
from loguru import logger


def request_data_to_company_create_draft(data: dict[str, Any], user_id: int) -> CompanyCreateDraft:
    """
    :raises KeyError:
    :raises ValidationError:
    """

    try:
        name: Any = data["name"]
        representative_id = user_id
        country_code: Any = data["country_code"]
        business_number: Any = data["business_number"]
        established_date: Any = data["established_date"]
        description: Any = data["description"]
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        raise KeyError("Missing required field.")

    return CompanyCreateDraft(
        name=name,
        representative_id=Id(value=representative_id),
        country_code=CountryCode(value=country_code),
        business_id=BusinessNumber(country_code=CountryCode(value=country_code), value=business_number),
        established_date=established_date,
        description=description,
    )
