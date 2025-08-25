"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="schoolmgmt API Documentation",
        default_version='v1',
        description="schoolmgmt API Description",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="contact@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # django admin
    path('admin/', admin.site.urls),
    
    # authentication
    path('api/v1/', include('users.api.v1.urls')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # include a route for Simple JWT’s TokenVerifyView 
    # if you wish to allow API users to verify HMAC-signed tokens without having access to your signing key
    # The TokenVerifyView provides no information about a token’s fitness for a particular use, 
    # it only verifies if a token is valid or not, and return a 200 or 401 status code respectively.
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # api
    path('api/v1/', include('colleges.api.v1.urls')),
    path('api/v1/', include('departments.api.v1.urls')),
    path('api/v1/', include('courses.api.v1.urls')),
    path('api/v1/', include('professors.api.v1.urls')),
    path('api/v1/', include('students.api.v1.urls')),
    path('api/v1/', include('subjects.api.v1.urls')),
    
    # Swagger
    path('api/v1/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
