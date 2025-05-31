from typing import Any

from application.converters.request_converters.company import request_data_to_company_create_draft
from application.draft.company import CompanyCreateDraft
from application.ports.service import AbstractAppService
from domain.models.company import Company
from domain.models.country import Country
from domain.services.company import CompanyService
from domain.services.country import CountryService
from domain.value_objects.common import Id
from domain.value_objects.company import CompanyCreatePayload
from loguru import logger


class CompanyAppService(AbstractAppService):
    def __init__(self, company_service: CompanyService, country_service: CountryService):
        self._company_service = company_service
        self._country_service = country_service

    def create(self, request_data: dict[str, Any], user_id: int) -> Company:
        """
        Creates a new company and assigns the specified user as its representative.

        Required request_data:
            - name: str
            - country_code: str (2-letter ISO code, e.g. "KZ")
            - business_number: str
            - established_date: str (ISO format "YYYY-MM-DD", must be in past)
            - description: Optional[str]

        Returns:
            Company: Created company entity with all fields populated

        Raises:
            KeyError: Missing required field
            ValidationError: Invalid data formats/values
            CountryNotFoundException: country_code doesn't exist
            UserNotFoundException: user_id doesn't exist
            ValidationException: Business rule violations:
                - Invalid business number format
                - Established date in future
        """
        draft: CompanyCreateDraft = request_data_to_company_create_draft(request_data, user_id)
        logger.debug("draft was parsed.")

        country: Country = self._country_service.get_country_by_code(draft.country_code)
        logger.debug(f"country_code = {country.code}")

        payload: CompanyCreatePayload = CompanyCreatePayload(
            name=draft.name,
            representative_id=draft.representative_id,
            country_id=Id(value=country.id),
            business_id=draft.business_id,
            established_date=draft.established_date,
            description=draft.description,
        )

        company: Company = self._company_service.create(payload)
        logger.info("Company created successfully.")

        return company
