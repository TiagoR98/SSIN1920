from django.shortcuts import render
from rest_framework import serializers, viewsets, routers, permissions
from .models import Resource
import requests
import jwt

# Create your views here.

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'url', 'data']

class ResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'Authorization' not in request.headers:
            return False

        token_string = request.headers['Authorization']
        token = jwt.decode(token_string, verify=False)
        print(token)

        r = requests.post('http://auth-server:8000/api/token/verify/', data={"token": token_string})
        if r.status_code != 200:
            return False

        if 'token_type' not in token:
            return False
        elif token['token_type'] != "access":
            return False

        return True

class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [ResourcePermission]


router = routers.DefaultRouter()
router.register(r'resources', ResourceViewSet)
