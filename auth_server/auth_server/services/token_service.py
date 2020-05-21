from auth_server.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

class TokenService:

    @staticmethod
    def add_token(client):
        generated_token = RefreshToken.for_user(client)

        token = Token(access=str(generated_token.access_token), refresh=str(generated_token), client=client)
        token.save()

        return token

    @staticmethod
    def check_access_token(token):
        return Token.objects.filter(access=token).filter(expiration__gt=datetime.now()).exists()
    
    @staticmethod
    def check_refresh_token(refresh, client):
        return Token.objects.filter(refresh=refresh).filter(client=client).exists()

    @staticmethod
    def refresh_token(refresh, client):
        old_token = Token.objects.filter(refresh=refresh).filter(client=client)
        old_token.delete()

        generated_token = RefreshToken.for_user(client)

        token = Token(access=str(generated_token.access_token), refresh=refresh, client=client)
        token.save()

        return token
