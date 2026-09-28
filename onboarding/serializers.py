from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'firstName', 'lastName', 'email', 'phone', 'home_country', 'campus_city', 'course', 'card_id', 'created_at']
        read_only_fields = ['id', 'card_id', 'created_at']


class StudentRegistrationSerializer(serializers.Serializer):
    """Serializer for student registration"""
    firstName = serializers.CharField(max_length=100)
    lastName = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=30)
    home_country = serializers.CharField(max_length=100)
    campus_city = serializers.CharField(max_length=100)
    course = serializers.CharField(max_length=120)

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student
