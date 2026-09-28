from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'students', views.StudentViewSet)

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # Include router URLs for ViewSets
    path('api/', include(router.urls)),
    
    # Custom API endpoints
    path('api/register-student/', views.register_student, name='register_student'),
    path('api/student/<int:student_id>/', views.get_student, name='get_student'),
    path('api/country-info/', views.get_country_info, name='country_info'),
    path('api/get-restaurants/', views.get_restaurants, name='get_restaurants'),
    path('api/generate-welcome-pack/', views.generate_welcome_pack, name='generate_welcome_pack'),
]