from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import File
from .serializers import FileSerializer

#TODO: need to make authentication_class and permissions_class modular
class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]



