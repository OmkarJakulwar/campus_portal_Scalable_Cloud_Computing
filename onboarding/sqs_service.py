import json
import boto3
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class SQSService:
    # Service to handle Amazon SQS queue operations
    
    def __init__(self):
        self.queue_url = settings.SQS_QUEUE_URL
        self.region = settings.AWS_REGION_NAME
        
        # Initialize SQS client
        self.sqs_client = boto3.client(
            'sqs',
            region_name=self.region,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            aws_session_token=settings.AWS_SESSION_TOKEN
        )
    
    def send_message(self, message_body):
        # Send a message to the SQS queue
        
        if not self.queue_url:
            logger.warning("SQS Queue URL not configured")
            return {'success': False, 'error': 'SQS Queue URL not configured'}
        
        try:
            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body)
            )
            logger.info(f"Message sent to SQS: {response.get('MessageId')}")
            return {
                'success': True,
                'message_id': response.get('MessageId')
            }
        except Exception as e:
            logger.error(f"Error sending message to SQS: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def send_welcome_pack_task(self, student_id):
        # Send a task to generate and send a welcome pack for a student
        
        message = {
            'task_type': 'generate_welcome_pack',
            'student_id': student_id
        }
        return self.send_message(message)
