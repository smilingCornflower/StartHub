from presentation.response_factories.common import CommonErrorResponseFactory


class PermissionErrorResponseFactory(CommonErrorResponseFactory):
    error_codes = CommonErrorResponseFactory.error_codes | {}
