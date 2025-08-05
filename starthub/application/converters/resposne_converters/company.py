from application.dto.geo import AddressDto
from application.dto.project import CompanyFounderDto, CompanyFullDto
from domain.models.company import Company


def company_to_dto(company: Company) -> CompanyFullDto:
    company_founder_dto = CompanyFounderDto(
        name=company.founder.name,
        surname=company.founder.surname,
        description=company.founder.description,
    )
    country_code: str = company.country.code
    if company.address is not None:
        address_dto = AddressDto(
            country_code=country_code,
            region_name=company.address.region.name,
            city_name=company.address.city.name,
            district=company.address.district,
            street=company.address.street,
            house_number=company.address.house_number,
            postal_code=company.address.postal_code,
            raw_address=company.address.raw_address,
        )
    else:
        address_dto = None

    return CompanyFullDto(
        id=company.id,
        name=company.name,
        slug=company.slug,
        founder=company_founder_dto,
        country_code=country_code,
        business_id=company.business_id,
        established_date=company.established_date,
        address=address_dto,
    )
