import random
import string
import datetime

from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect

from auth_server.services.login_service import LoginService
from auth_server.models import AuthorizationCode


class AuthorizationView(APIView):

    scopes = ["read","write","delete"]

    def get(self, request):
        error = ""

        if not AuthorizationView.validate_authorization_request(request):
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "invalid_request"))

        print(request.GET['scope'])
        received_scopes = request.GET['scope'].split(" ")
        received_scopes = received_scopes[:-1]

        if not all(elem in AuthorizationView.scopes  for elem in received_scopes) or len(received_scopes) == 0:
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "invalid_scope"))

        if request.GET['response_type'] != "code":
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "unsupported_response_type"))

        return render(request, 'authorize.html', {'client_id': request.GET['client_id'],
                                                  'redirect_uri': request.GET['redirect_uri'],
                                                  'scope': request.GET['scope'],
                                                  'scope_list': received_scopes,
                                                  'state': request.GET['state']})


    def post(self, request):
        if LoginService.check_credentials(request.POST['username'], request.POST['password']):
            code = AuthorizationView.generate_authorization_code(request.GET['client_id'], request.GET['redirect_uri'], request.GET['scope'])
            return redirect("{}?code={}&state={}".format(request.GET['redirect_uri'], code, request.GET['state']))
        else:
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "access_denied"))


    @staticmethod
    def generate_authorization_code(client_id, redirect_uri, scope):
        lettersAndDigits = string.ascii_letters + string.digits
        code = ''.join((random.choice(lettersAndDigits) for i in range(15)))
        now = datetime.datetime.now()
        expiration = now + datetime.timedelta(minutes=10)
        new_code = AuthorizationCode(code=code, client_id=client_id, scope=scope, redirect_uri=redirect_uri,expiration=expiration)
        new_code.save()

        return new_code.code


    @staticmethod
    def validate_authorization_request(request):
        if 'response_type' not in request.GET:
           return False

        if 'client_id' not in request.GET:
           return False

        if 'redirect_uri' not in request.GET:
           return False

        if 'scope' not in request.GET:
           return False

        if 'state' not in request.GET:
           return False

        return True

class AddAccountView(APIView):

    def post(self, request):
        LoginService.add_credentials(request.POST['username'], request.POST['password'])

        return HttpResponse(status=204)
