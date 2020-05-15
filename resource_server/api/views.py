from django.shortcuts import render
from rest_framework import serializers, viewsets, routers, permissions
from .models import Resource
import requests

# Create your views here.

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'url', 'data']

class ResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if 'Authorization' not in request.headers:
            return False

        r = requests.post('http://auth-server:8000/api/token/verify/', data={"token": request.headers['Authorization']})
        if r.status_code != 200:
            return False

        return (request.method in permissions.SAFE_METHODS)

class ResourceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [ResourcePermission]


router = routers.DefaultRouter()
router.register(r'resources', ResourceViewSet)
