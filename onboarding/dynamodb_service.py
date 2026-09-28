import boto3
from datetime import datetime, timezone

from django.conf import settings

class DynamoDBService:
    def __init__(self):
        region = getattr(settings, "AWS_REGION_NAME", None) or getattr(settings, "AWS_REGION", None)
        if not region:
            raise ValueError("AWS region is not configured.")

        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.table = self.dynamodb.Table('CountryInsights')

    def save_student(self, student):
        table = self.dynamodb.Table('Students')

        table.put_item(
            Item={
                'id': student.id,
                'firstName': student.firstName,
                'lastName': student.lastName,
                'email': student.email,
                'phone': student.phone,
                'home_country': student.home_country,
                'campus_city': student.campus_city,
                'course': student.course,
                'card_id': student.card_id
            }
        )

    def save_welcome_pack(self, student_id):
        table = self.dynamodb.Table('WelcomePack')
        datetime.now(timezone.utc)
        timestamp = 1571595618.0
        table.put_item(
            Item={
                'student_id': str(student_id),
                'generated_at': datetime.fromtimestamp(timestamp, timezone.utc)
            }
        )