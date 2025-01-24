from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from nasac import settings

schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
      description="Your API Description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="your-email@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('core/', include('core.urls')),
]

for app in settings.APPS if 'APPS' in settings.configs.keys() else []:
    urlpatterns.append(path(f"{app}/", include(f"{app}.urls")))
