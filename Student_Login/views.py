from django.shortcuts import render, redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from onboarding.models import Student

from .serializers import StudentAccountRegistrationSerializer, StudentAccountLoginSerializer
from .dynamodb_service import StudentAuthService


@api_view(['POST'])
def register_account_api(request):
    
    serializer = StudentAccountRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.validated_data['username']
        service = StudentAuthService()
        existing = service.get_account(username)
        if existing:
            return Response({'error': 'Username already taken.'}, status=status.HTTP_400_BAD_REQUEST)
        student_id = serializer.validated_data.get('student_id')
        service.create_account(username, serializer.validated_data['password'], student_id)
        return Response({'message': 'Account created successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def student_login_api(request):
    
    serializer = StudentAccountLoginSerializer(data=request.data)
    
    if serializer.is_valid():
        service = StudentAuthService()
        account = service.verify_credentials(
            serializer.validated_data['username'],
            serializer.validated_data['password']
        )
        if account:
            request.session['student_username'] = account['username']
            
            student_id = account.get('student_id')
            if student_id is not None:
                try:
                    request.session['student_id'] = int(student_id)
                except (TypeError, ValueError):
                    request.session['student_id'] = str(student_id)
            return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def student_logout_api(request):

    request.session.flush()
    return Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)

# HTML Views

def register_account_page(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        student_id = request.POST.get('student_id') or None
        service = StudentAuthService()

        if service.get_account(username):
            
            return render(request, 'Student_Login/register.html', {
                'error': 'Username already taken.',
                'username': username,
                'student_id': student_id,
            })

        service.create_account(username, password, student_id)
        return redirect('student_login')
  
    return render(request, 'Student_Login/register.html')


def student_login_page(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        service = StudentAuthService()
        account = service.verify_credentials(username, password)

        if account:
            # Successful login: save session values
            request.session['student_username'] = account['username']
             
            student_id = account.get('student_id')
            if student_id is not None:
                try:
                    request.session['student_id'] = int(student_id)
                    
                     # Fetch student and store full name
                    student = Student.objects.filter(id=student_id).first()
                    if student:
                        full_name = f"{student.firstName} {student.lastName}"
                        request.session['student_name'] = full_name
                        
                except (TypeError, ValueError):
                    request.session['student_id'] = str(student_id)

            # Redirect to the home
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect(resolve_url('index'))
        
        return render(request, 'Student_Login/login.html', {
            'error': 'Invalid username or password.',
            'username': username,
        })
    
    return render(request, 'Student_Login/login.html')


def student_logout_page(request):
    
    request.session.flush()
    return redirect('student_login')