from myapp.serializer.auth_serializer import AuthenticateSerializer
import inject


class TokenBase:
    def generate_token(self, request):
        serializer = AuthenticateSerializer(data=request)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            raise e
        data = serializer.validated_data
        return data['token']


def token_bash_config(binder: inject.Binder):
    binder.bind(TokenBase, TokenBase())
