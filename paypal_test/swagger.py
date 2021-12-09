from django.conf.urls import url
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_auth.serializers import TokenSerializer
from rest_framework import permissions, status
from rest_auth.views import LoginView
from django.conf import settings

from users.serializers import TokenSerializerCustom

schema_view = get_schema_view(
    openapi.Info(
        title="CCL API",
        default_version='v1',
        description="Application for streaming Robot fights",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

decorated_login_view = swagger_auto_schema(
    method='post',
    operation_description='Check the credentials and return the REST Token '
                          'if the credentials are valid and authenticated.',
    responses={status.HTTP_200_OK: TokenSerializer}
)(LoginView.as_view())

swagger_urls = []

if settings.SHOW_SWAGGER:
    swagger_urls = [
        url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        url(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), ]
