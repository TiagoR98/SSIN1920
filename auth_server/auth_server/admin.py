from django.contrib import admin
from auth_server.models import User, Client, Token, AuthorizationCode

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Token)
admin.site.register(AuthorizationCode)
