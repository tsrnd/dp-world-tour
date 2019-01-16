import inject, json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from shared.common_response import *


class BaseHandler:
    import logging
    logger = logging.getLogger(__name__)

    def validate(self, serializer, request):
        formCheck = serializer(data=request)
        if not formCheck.is_valid():
            response = ValidateResponse
            response["fields"] = formCheck.errors
            response = Response(
                response,
                content_type='application/json',
                status=status.HTTP_400_BAD_REQUEST,
            )
            response.accepted_renderer = JSONRenderer()
            response.accepted_media_type = 'application/json'
            response.renderer_context = {}
            return response
        else:
            return None

    def not_found_response(self):
        response = NotFoundResponse
        response = Response(
            NotFoundResponse,
            content_type='application/json',
            status=status.HTTP_404_NOT_FOUND,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response

    def internal_server_response(self):
        response = Response(
            InternalResponse,
            content_type='application/json',
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response

    def forbidden_response(self):
        response = Response(
            ForbiddenResponse,
            content_type='application/json',
            status=status.HTTP_403_FORBIDDEN,
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = 'application/json'
        response.renderer_context = {}
        return response

    def log_info(self, message):
        self.logger.info(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)        

    
def bh_config(binder: inject.Binder):
    binder.bind(BaseHandler, BaseHandler())
