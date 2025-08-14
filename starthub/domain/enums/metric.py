from enum import StrEnum


class MetricEnum(StrEnum):
    LTV = "ltv"
    ARPU = "arpu"
    ARPPU = "arppu"
    CAC = "cac"
    NPS = "nps"
    ROI = "roi"
    AOV = "aov"
    CHURN_RATE = "churn_rate"
    RETENTION_RATE = "retention_rate"
    CONVERSION_RATE = "conversion_rate"


class MetricDisplayEnum(StrEnum):
    LTV = "LTV"
    ARPU = "ARPU"
    ARPPU = "ARPPU"
    CAC = "CAC"
    NPS = "NPS"
    ROI = "ROI"
    AOV = "AOV"
    CHURN_RATE = "Churn Rate"
    RETENTION_RATE = "Retention Rate"
    CONVERSION_RATE = "Conversion Rate"
