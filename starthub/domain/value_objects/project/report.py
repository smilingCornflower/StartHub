from domain.constants import PROJECT_REJECTED_REPORT_MAX_LENGTH
from domain.ports.payload import AbstractCreatePayload, AbstractUpdatePayload
from domain.value_objects.common import Id, StringVo


class ProjectReportId(Id):
    pass


class ProjectReportContent(StringVo):
    max_length = PROJECT_REJECTED_REPORT_MAX_LENGTH


class ProjectReportCreatePayload(AbstractCreatePayload):
    pass


class ProjectUpdatePayload(AbstractUpdatePayload):
    pass
