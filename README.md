# Campus Portal – Student Onboarding Application

Campus Portal is a Django-based web application designed to simplify the onboarding process for new university students.  
The platform integrates multiple external APIs and AWS cloud services to provide useful information such as student profiles, country insights, restaurant recommendations, and automated welcome packs.


# Features

## Student Registration
Students can register by providing basic details such as name, email, phone number, course, home country, and campus city.

Once registered, the system automatically generates a **Digital ID Card** using an external API.

## Student Profile
After registration, the portal displays the student's information including:

- Name
- Email
- Phone number
- Course
- Home country
- Campus city
- Generated card ID

Students can also download their digital ID card.

## Country Insights
The system integrates with the **REST Countries API** to show useful information about the student's home country, including:

- Currency
- Timezone
- Country flag
- Basic country details

## Restaurant Recommendations
Students can discover restaurants near their campus city using a **Restaurant Recommendation API**.

Filters include:
- City
- Cuisine
- Budget
- Rating

Restaurant locations can also be displayed on a map using latitude and longitude.

## Welcome Pack Generation
The application supports **asynchronous welcome pack generation** using AWS services.

Workflow:

1. The application sends a request to **Amazon SQS**
2. **AWS Lambda** processes the request
3. The welcome pack is generated in the background

This design makes the system scalable and cloud-ready.

---

# Technology Stack

### Backend
- Django 
- Django REST Framework

### Frontend
- HTML
- Bootstrap 5
- JavaScript

### Database
- SQLite (development)
- MySQL / AWS DynamoDB (production ready)

### External APIs
- Digital ID Card API
- REST Countries API
- Restaurant Recommendation API

### AWS Services
- Amazon SQS
- AWS Lambda
- AWS RDS (optional)

---

# Installation

## 1. Clone the repository

```bash
git clone <repository-url>
cd campus_portal 


## 2. Create Virtual Environment:
```bash
python -m venv .venv

## 3. Activate it:
```bash
Windows: .venv\Scripts\activate
macOS/Linux: source .venv/bin/activate

## 4. Install dependencies:
```bash
pip install -r requirements.txt

## 6. Run Database Migration
```bash
python manage.py makemigrations
python manage.py migrate

## 7. Run the development server
```bash
python manage.py runserver

## 8. Open the application on
http://localhost:8000