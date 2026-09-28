import boto3
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password


class StudentAuthService:
    # Provide CRUD and verification operations for student login accounts.

    def __init__(self):
        self.table_name = 'StudentAccounts'
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=settings.AWS_REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=getattr(settings, 'AWS_SESSION_TOKEN', None),
        )
        self.table = self.dynamodb.Table(self.table_name)

    def create_account(self, username: str, password: str, student_id: int | None = None) -> bool:
        """Insert a new student account record into DynamoDB."""
        hashed = make_password(password)
        item = {
            'username': username,
            'password': hashed,
        }
        if student_id is not None:
            item['student_id'] = int(student_id)
        self.table.put_item(Item=item)
        return True

    def get_account(self, username: str) -> dict | None:
        response = self.table.get_item(Key={'username': username})
        return response.get('Item')

    def verify_credentials(self, username: str, password: str) -> dict | None:
        account = self.get_account(username)
        if not account:
            return None
        if check_password(password, account.get('password', '')):
            if 'student_id' in account:
                try:
                    account['student_id'] = int(account['student_id'])
                except (TypeError, ValueError):
                    pass
            return account
        return None