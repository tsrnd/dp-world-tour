import inject, json

from django.http import HttpResponse
from django.views import View


class AuthHandler(View):
    def post(self, request):
        return HttpResponse(
            json.dumps({"message": "Success"}),
            status=200,
            content_type='application/json'
        )
