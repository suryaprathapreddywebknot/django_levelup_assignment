from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="RazorpayService API",
        default_version='v1',
        description="API documentation for RazorpayService",
        # terms_of_service="https://www.yourapp.com/terms/",
        # contact=openapi.Contact(email="contact@yourapp.com"),
        # license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=()
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authapp.urls')),
    path('api/', include('documentsapp.urls')),
    path('api/', include('attendenceapp.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


