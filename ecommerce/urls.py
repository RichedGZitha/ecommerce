"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Ecommerce API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://equitek.herokuapp.com",
      contact=openapi.Contact(email="equitekconsulting@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   #permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^auth/v1/', include('djoser.urls')),
    url(r'^auth/v1/', include('djoser.urls.jwt')),
    path('', include('main.urls')),

    path('docs/api/?format=.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/api/?format=.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('docs/api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('products/', include('products.urls')),
    path('transactions/', include('transactions.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)