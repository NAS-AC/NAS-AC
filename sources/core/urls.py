import importlib

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FileViewSet
from django.conf.urls.static import static
from nasac import settings

user_view_set = importlib.import_module(settings.AUTHENTICATION_APP + '.authentication')
UserViewSet = getattr(user_view_set, 'UserViewSet')

router = DefaultRouter()
router.register(r'files', FileViewSet, basename='file')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)