from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# Create router for viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet)

app_name = 'users_v1'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # JWT token endpoint (alternative login)
    path('auth/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Profile management
    path('auth/profile/', views.profile, name='profile'),
    path('auth/profile/update/', views.update_profile, name='update_profile'),
    path('auth/change-password/', views.change_password, name='change_password'),
    
    # User management (admin/principal access)
    path('', include(router.urls)),
]
