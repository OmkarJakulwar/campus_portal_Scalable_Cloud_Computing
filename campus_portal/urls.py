
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('onboarding.urls')),
    path('student_accounts/', include('Student_Login.urls')),
]
