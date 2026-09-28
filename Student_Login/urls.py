from django.urls import path
from . import views

urlpatterns = [
    # HTML pages
    path('register/', views.register_account_page, name='student_register'),
    path('login/', views.student_login_page, name='student_login'),
    path('logout/', views.student_logout_page, name='student_logout_page'),

    # API endpoints
    path('api/register/', views.register_account_api, name='register_account_api'),
    path('api/login/', views.student_login_api, name='student_login_api'),
    path('api/logout/', views.student_logout_api, name='student_logout_api'),
]