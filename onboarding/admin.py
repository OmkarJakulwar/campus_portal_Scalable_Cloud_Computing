from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstName', 'lastName', 'email', 'campus_city', 'course', 'cardId')
    search_fields = ('firstName', 'lastName', 'email', 'campus_city', 'home_country')