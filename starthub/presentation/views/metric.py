from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.enums.metric import MetricDisplayEnum


class MetricView(APIView):
    def get(self, request: Request) -> Response:
        all_metrics = [m.value for m in MetricDisplayEnum]

        return Response(all_metrics, status=status.HTTP_200_OK)
