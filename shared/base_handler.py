import inject, json

from django.http import HttpResponse
from shared.common_response import *


class BaseHandler:
    import logging
    logger = logging.getLogger(__name__)

    def validate(self, form, request):
        formCheck = form(request)
        if not formCheck.is_valid():
            response = ValidateResponse
            response["fields"] = json.loads(formCheck.errors.as_json(escape_html=False))
            
            return HttpResponse(
                json.dumps(response),
                status=400,
                content_type='application/json'
            )
        else:
            return None
                

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)        

    
def bh_config(binder: inject.Binder):
    binder.bind(BaseHandler, BaseHandler())
