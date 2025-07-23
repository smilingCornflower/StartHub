from pprint import pformat

from loguru import logger
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class TestView(APIView):
    @staticmethod
    def get(request: Request) -> Response:
        print("=" * 100)
        logger.debug(f"Host: {request.get_host()}")
        logger.debug(f"Remote Addr: {request.META.get('REMOTE_ADDR')}")
        logger.debug(f"Headers: \n{pformat({k: v for k, v in request.META.items() if k.startswith('HTTP_')})}")
        logger.debug(f"Cookies: {request.COOKIES}")

        return Response(status=200)
