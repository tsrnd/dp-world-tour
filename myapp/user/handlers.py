import inject, json, logging

from django.http import HttpResponse
from django.views import View

logger = logging.getLogger(__name__)


class AuthHandler(View):
    def post(self, request):
        logger.info("test")
        return HttpResponse(
            json.dumps({"message": "Success"}),
            status=200,
            content_type='application/json'
        )
