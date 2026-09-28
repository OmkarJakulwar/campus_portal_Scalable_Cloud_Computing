# Campus Portal – Scalable Student Onboarding on AWS

Campus Portal is a cloud-hosted web application that helps new university students get set up on day one. A student creates an account, registers their details, and immediately gets a **digital student ID card**, information about their **home country**, **restaurant recommendations** near campus, and a **welcome pack** that is generated in the background.

The project was built to practise **scalable cloud application design**. The portal itself is kept small. Heavy or independent work goes to separate services: serverless APIs on AWS Lambda, a message queue (Amazon SQS), and managed NoSQL storage (Amazon DynamoDB). Each part can then scale on its own.

---

## Key Highlights

- **Microservice integration**: the portal uses three independent REST APIs:
  - **Contact / ID Card Generator API**: built by me, deployed on AWS Lambda + API Gateway ([repository](https://github.com/OmkarJakulwar/contact_id_card_generator_api))
  - **Restaurant Recommendation API**: built by a colleague, deployed on AWS API Gateway
  - **REST Countries API**: a public third-party API
- **Asynchronous processing**: welcome pack requests are pushed to **Amazon SQS** and processed in the background, so users never wait on slow work.
- **Serverless + managed data**: student records, login accounts and welcome packs are stored in **Amazon DynamoDB**.
- **Containerised deployment**: Docker image → **Amazon ECR** → **AWS Elastic Beanstalk**, served by Gunicorn.
- **CI/CD**: GitHub Actions runs a **SonarQube Cloud** quality scan and, when it passes, builds, pushes and deploys automatically on every push to `main`.
- **Secure configuration**: secrets and endpoints come from environment variables. Passwords are stored as salted hashes (Django's PBKDF2).

---

## Features

| Feature | What it does | Service behind it |
|---|---|---|
| Student accounts | Sign up / log in / log out with session-based auth | DynamoDB (`StudentAccounts` table) |
| Student registration | Registers a student and blocks duplicate emails | Django ORM + DynamoDB (`Students` table) |
| Digital ID card | Generates a unique card ID, QR code and card image the student can download | ID Card Generator API (AWS Lambda) |
| Country insights | Shows flag, capital, currency, languages, timezones and population of the home country | REST Countries API |
| Restaurant finder | Recommends restaurants by city, cuisine, budget and minimum rating | Restaurant Recommendation API (colleague's service) |
| Welcome pack | Queues a background task and shows a combined pack (profile + country + restaurants) | Amazon SQS → AWS Lambda |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django 5, Django REST Framework |
| Frontend | HTML, Bootstrap 5, vanilla JavaScript (Fetch API) |
| Databases | Amazon DynamoDB, MySQL / Amazon RDS (optional), SQLite (local development) |
| Messaging | Amazon SQS |
| Compute | AWS Elastic Beanstalk (Docker), AWS Lambda |
| Container registry | Amazon ECR |
| External APIs | ID Card Generator API, Restaurant Recommendation API, REST Countries API |
| DevOps | Docker, Gunicorn, WhiteNoise, GitHub Actions, SonarQube Cloud |
| AWS SDK | boto3 |

---

## How It Works

1. **Login**: the student signs up or logs in. Credentials are checked against DynamoDB and a Django session is created. The dashboard is only available to logged-in students.
2. **Registration**: the portal validates the form, then calls the **ID Card Generator API**. When a card ID comes back, the student is saved in the relational database and copied to DynamoDB. The card image is returned to the browser for download.
3. **Country info and restaurants**: the dashboard calls the portal's REST endpoints. Those endpoints call the **REST Countries** and **Restaurant Recommendation** APIs.
4. **Welcome pack**: the portal puts a `generate_welcome_pack` message on **SQS** and returns `202 Accepted` right away. A Lambda consumer handles the message in the background.

Every external call goes through its own small service class (`id_service.py`, `country_service.py`, `restaurant_service.py`, `sqs_service.py`, `dynamodb_service.py`). Each class has timeouts and error handling, so one failing API does not break the whole page.

---

## Scalability Approach

- **Stateless web tier**: the Django container keeps no local state, so Elastic Beanstalk can run more instances behind its load balancer as traffic grows. Each container runs several Gunicorn workers.
- **Independent services**: the ID card and restaurant APIs run on AWS Lambda. They scale automatically and separately from the portal, and each one can be updated or replaced without touching the others.
- **Queue-based decoupling**: SQS absorbs traffic spikes. Welcome pack jobs wait in the queue and are processed by Lambda in parallel batches, so the web tier stays fast.
- **Managed NoSQL storage**: DynamoDB handles high read/write throughput without any database servers to manage.
- **Config-driven integration**: every API endpoint is an environment variable. Adding a new external API means adding a new service class and a setting.

---

## Project Structure

```
campus_portal/            # Django project settings and root URLs
onboarding/               # Registration, ID card, country, restaurant and welcome pack features
  ├── id_service.py         # Client for the ID Card Generator API
  ├── country_service.py    # Client for the REST Countries API
  ├── restaurant_service.py # Client for the Restaurant Recommendation API
  ├── sqs_service.py        # Sends welcome pack tasks to Amazon SQS
  ├── dynamodb_service.py   # Writes students / welcome packs to DynamoDB
  ├── views.py              # REST API endpoints
  └── templates/, static/   # Dashboard UI
Student_Login/            # Student sign-up / login backed by DynamoDB
Dockerfile, entrypoint.sh # Container image (migrate → collectstatic → gunicorn)
.github/workflows/        # CI/CD: SonarQube scan → build → ECR → Elastic Beanstalk
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register-student/` | Register a student and generate their ID card |
| GET | `/api/student/<id>/` | Get a student's details |
| GET | `/api/country-info/?country=<name>` | Get home country information |
| POST | `/api/get-restaurants/` | Get restaurant recommendations (`city`, `cuisine`, `budget`, `min_rating`) |
| POST | `/api/generate-welcome-pack/` | Queue a welcome pack task (`student_id`) |
| GET/POST/PUT/DELETE | `/api/students/` | CRUD for students (DRF ViewSet) |
| POST | `/student_accounts/api/register/` | Create a login account |
| POST | `/student_accounts/api/login/` | Log in |
| POST | `/student_accounts/api/logout/` | Log out |

---

## Getting Started

### Prerequisites
- Python 3.12+
- An AWS account with DynamoDB tables (`Students`, `StudentAccounts`, `WelcomePack`) and an SQS queue
- (Optional) Docker

### 1. Clone and install

```bash
git clone https://github.com/OmkarJakulwar/campus_portal_Scalable_Cloud_Computing.git
cd campus_portal_Scalable_Cloud_Computing

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database: sqlite (default) or mysql
DB_ENGINE=sqlite
# MYSQL_DB=campus_portal_db
# MYSQL_USER=django_user
# MYSQL_PASSWORD=...
# MYSQL_HOST=...
# MYSQL_PORT=3306

# AWS
AWS_REGION_NAME=us-east-1
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_SESSION_TOKEN=...
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<account-id>/<queue-name>

# External APIs
ID_CARD_API_URL=https://<api-id>.execute-api.us-east-1.amazonaws.com/card/generate
RESTAURANT_API_URL=https://<api-id>.execute-api.us-east-1.amazonaws.com/recommend
COUNTRY_API_URL=https://restcountries.com/v3.1/name/
```

### 3. Run locally

```bash
python manage.py migrate
python manage.py runserver
```

Open http://localhost:8000. You will be redirected to the login page. Create an account and start onboarding.

### 4. Run with Docker

```bash
docker build -t campus-portal .
docker run -p 8080:8080 --env-file .env campus-portal
```

Open http://localhost:8080.

---

## Deployment (CI/CD)

Every push to `main` triggers the GitHub Actions workflow:

1. **Quality gate**: installs dependencies and runs a **SonarQube Cloud** scan.
2. **Build**: builds the Docker image, tagged with the commit SHA.
3. **Push**: pushes the image to **Amazon ECR**.
4. **Deploy**: creates a `Dockerrun.aws.json` bundle and deploys it to **AWS Elastic Beanstalk**.

Required GitHub secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION`, `ECR_REPOSITORY`, `EB_APPLICATION_NAME`, `EB_ENVIRONMENT_NAME`, `DJANGO_SECRET_KEY`, `SONAR_TOKEN`.

---

## Future Improvements

- Call the country and restaurant APIs **in parallel**, on the server with a thread pool or async views and in the browser with `Promise.all`, to cut dashboard load time.
- **Cache** country data (ElastiCache / Redis) because it rarely changes.
- Add **retries with backoff** and a **dead-letter queue** for failed SQS jobs.
- Replace static AWS keys with **IAM roles** on Elastic Beanstalk.
- Add unit tests for the service classes, with mocked AWS services and APIs.
- Add monitoring and alarms with **Amazon CloudWatch**.

---

## Related Repositories

- [Contact / ID Card Generator API](https://github.com/OmkarJakulwar/contact_id_card_generator_api): the FastAPI microservice this portal uses to generate student ID cards.

## Author

**Omkar Jakulwar**. Built as an academic project for the *Scalable Cloud Computing* module.
