from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect

from auth_server.services.login_service import LoginService


class AuthorizationView(APIView):
    def get(self, request):
        error = ""

        if not AuthorizationView.validate_authorization_request(request):
            error = "invalid_request"

        return render(request, 'authorize.html', {'client_id': request.GET['client_id'],
                                                  'redirect_uri': request.GET['redirect_uri'],
                                                  'scope': request.GET['scope'],
                                                  'scope_list': request.GET['scope'].split(" "),
                                                  'state': request.GET['state']})


    def post(self, request):
        if LoginService.check_credentials(request.POST['username'], request.POST['password']):
            return redirect("{}?code={}&state={}".format(request.GET['redirect_uri'], "oijeofierjgoreijer", request.GET['state']))
        else:
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "access_denied"))





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
