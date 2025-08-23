from domain.models.geo.city import City
from domain.models.geo.region import Region
from modeltranslation.translator import TranslationOptions, register


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("name",)
