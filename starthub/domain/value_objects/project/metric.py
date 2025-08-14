from domain.value_objects import BaseVo


class Ltv(BaseVo):
    value: float


class Arpu(BaseVo):
    value: float


class Arppu(BaseVo):
    value: float


class Cac(BaseVo):
    value: float


class Nps(BaseVo):
    value: float


class Roi(BaseVo):
    value: float


class Aov(BaseVo):
    value: float


class ChurnRate(BaseVo):
    value: float


class RetentionRate(BaseVo):
    value: float


class ConversionRate(BaseVo):
    value: float
