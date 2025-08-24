from presentation.response_factories.common import CommonErrorResponseFactory


class NotificationErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
