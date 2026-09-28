from rest_framework import serializers


class StudentAccountRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    student_id = serializers.IntegerField(required=False, allow_null=True)


class StudentAccountLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)