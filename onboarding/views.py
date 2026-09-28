from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer, StudentRegistrationSerializer
from .id_service import DigitalIDCardService
from .country_service import CountryInfoService
from .restaurant_service import RestaurantRecommendationService
from .sqs_service import SQSService
import logging
from .dynamodb_service import DynamoDBService

logger = logging.getLogger(__name__)

dynamo_service = DynamoDBService()

STUDENT_NOT_FOUND = "Student not found"

def index(request):
    # Render the index/dashboard template
    if 'student_username' not in request.session:
        login_url = reverse('student_login')
        return redirect(f"{login_url}?next={request.path}")
    return render(request, 'index.html')


@api_view(['POST'])
def register_student(request):
    serializer = StudentRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        try:
            email = serializer.validated_data['email']

            if Student.objects.filter(email=email).exists():
                return Response(
                    {'error': 'A student with this email already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            id_service = DigitalIDCardService()
            card_response = id_service.generate_card_id(
                serializer.validated_data['firstName'],
                serializer.validated_data['lastName'],
                serializer.validated_data['email'],
                serializer.validated_data['phone'],
                serializer.validated_data['campus_city'],
                serializer.validated_data['home_country']
            )

            if not card_response.get('success') or not card_response.get('cardId'):
                return Response(
                    {
                        'error': 'Failed to generate ID card',
                        'details': card_response.get('error')
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.validated_data['card_id'] = card_response.get('cardId')
            student = serializer.save()
            dynamo_service.save_student(student)

            response_serializer = StudentSerializer(student)
            response_data = response_serializer.data

            # include card image from external ID card API response
            response_data['cardImageDataUrl'] = card_response.get('cardImageDataUrl')

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error in student registration: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_student(request, student_id):
    
    # Get student details by ID
    # GET /api/student/<id>
    
    try:
        student = Student.objects.get(id=student_id)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({'error': STUDENT_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_country_info(request):
    #    Get country information for a given country name.
    # GET /api/country-info?country=country_name
    
    country = request.query_params.get('country')

    if not country:
        return Response(
            {'error': 'country parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        service = CountryInfoService()
        info = service.get_country_info(country)

        if info.get('success'):
            return Response(info, status=status.HTTP_200_OK)

        return Response(info, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching country info: {str(e)}")
        return Response(
            {'success': False, 'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def get_restaurants(request):
    # Get restaurant recommendations
    # POST /api/get-restaurants

    try:
        cuisine = request.data.get('cuisine')
        budget = request.data.get('budget')
        min_rating = request.data.get('min_rating')
        city = request.data.get('city')

        service = RestaurantRecommendationService()
        result = service.get_restaurants(
            city=city,
            cuisine=cuisine,
            budget=budget,
            min_rating=min_rating
        )

        if result.get('success'):
            return Response(result)
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        logger.error(f"Error fetching restaurants: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def generate_welcome_pack(request):
    # Generate welcome pack asynchronously via SQS
    # POST /api/generate-welcome-pack
    
    student_id = request.data.get('student_id')
    
    if not student_id:
        return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Verify student exists
        student = Student.objects.get(id=student_id)
        
        # Send SQS message
        if not student:
            return Response({'error': STUDENT_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
        sqs_service = SQSService()
        result = sqs_service.send_welcome_pack_task(student_id)
        print("message send to sqs successfully")
        
        if result.get('success'):
            return Response({
                'message': 'Welcome pack generation initiated',
                'task_id': result.get('message_id')
            }, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Student.DoesNotExist:
        return Response({'error': STUDENT_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error generating welcome pack: {str(e)}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StudentViewSet(viewsets.ModelViewSet):
   # ViewSet for CRUD operations on Student model
  
    queryset = Student.objects.all()
    serializer_class = StudentSerializer