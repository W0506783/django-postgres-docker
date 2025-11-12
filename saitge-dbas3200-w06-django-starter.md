![alt text](image.png)

---

### **Workshop Details**

| Field                 | Information                                                                                                                                                       |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Course**            | DBAS 3200 – Data-Driven Application Programming                                                                                                                   |
| **Week**              | 6                                                                                                                                                                 |
| **Workshop Title**    | Designing a Maintainable & Testable Django Data Access Layer (DAL)                                                                                                |
| **Instructor**        | Davis Boudreau                                                                                                                                                    |
| **Estimated Time**    | 3 hours                                                                                                                                                           |
| **Pre-Requisites**    | MP1 complete (Docker stack, ORM CRUD), Python + SQL fundamentals                                                                                                  |
| **Software Required** | VSCode, Docker Desktop, pgAdmin, Python 3.11+, Django 5, DRF, pytest-django                                                                                       |
| **Purpose**           | To design and implement a structured Data Access Layer in Django that is maintainable, testable, and transaction-safe, using a Dockerized PostgreSQL environment. |

---

## **1. Workshop Overview**

In this workshop, you’ll elevate your Django skills from basic CRUD operations to **professional, modular architecture**.
You’ll learn to:

* Organize data logic into reusable components (Managers, QuerySets, Services).
* Implement **transactional safety** using `@transaction.atomic`.
* Expose a clean, testable API using Django REST Framework (DRF).
* Use **Docker + Makefile automation** for consistency and professionalism.

> 🎓 *This workshop simulates an industry workflow — it’s the foundation for MP2 and your final capstone.*

---

## **2. Learning Outcomes Addressed**

* **Outcome 1:** Implement a Data Access Layer (ORM).
* **Outcome 4:** Manipulate data within the application.
* **Outcome 5:** Exercise application-level transactional control.
* **Outcome 6:** Develop professionalism through structured workflow.
* **Outcome 7:** Enhance your portfolio with technical artifacts.

---

## **3. Background Knowledge**

Before you begin, review the key ideas behind this workshop.

| Concept                         | Why It Matters                                  | You’ll Apply It By...                            |
| ------------------------------- | ----------------------------------------------- | ------------------------------------------------ |
| **Dockerized Stack**            | Ensures everyone works in the same environment. | Running Postgres, Django, pgAdmin in containers. |
| **Data Access Layer (DAL)**     | Centralizes all data logic for easier testing.  | Building Managers/Services for clean separation. |
| **Transactional Safety**        | Prevents partial updates and data corruption.   | Using `@transaction.atomic` in service classes.  |
| **Testability**                 | Good code is verifiable.                        | Writing pytest-django unit tests on DAL logic.   |
| **DRF (Django REST Framework)** | Enables front-end integration via APIs.         | Creating serializers and viewsets for CRUD.      |

---

## **4. Activity Instructions**

### **Step 0 – Django Start: Build Your Project Foundation**

> 🔹 *Always begin in a clean folder to avoid conflicts.*

```bash
mkdir dbas3200_django_dal
cd dbas3200_django_dal
```

Create the following files inside this folder.

---

### **A. .env (environment configuration)**

```env
POSTGRES_DB=event_mgmt_wk6
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
DB_HOST=db
DJANGO_SECRET_KEY=dev-secret-change-me
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=*
WEB_PORT=8000
PGADMIN_PORT=5050
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin
```

---

### **B. docker-compose.yml**

This orchestrates the full stack: PostgreSQL, pgAdmin, and Django web app.

```yaml
version: "3.9"
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    ports: ["${POSTGRES_PORT}:5432"]
    volumes: ["pg_data:/var/lib/postgresql/data"]

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_DEFAULT_EMAIL}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_DEFAULT_PASSWORD}
    ports: ["${PGADMIN_PORT}:80"]
    depends_on: [db]

  web:
    build: .
    command: bash -lc "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    environment:
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DJANGO_DEBUG: ${DJANGO_DEBUG}
      DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS}
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_HOST: ${DB_HOST}
      POSTGRES_PORT: ${POSTGRES_PORT}
    volumes: [".:/app"]
    ports: ["${WEB_PORT}:8000"]
    depends_on: [db]

volumes:
  pg_data:
```

---

### **C. Dockerfile**

A minimal Django development image that installs dependencies and runs the dev server.

```dockerfile
FROM python:3.12-slim

RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["bash","-lc","python manage.py runserver 0.0.0.0:8000"]
```

---

### **D. requirements.txt**

```
Django==5.1.1
psycopg2-binary==2.9.9
python-dotenv==1.0.1
djangorestframework==3.15.2
django-cors-headers==4.4.0
pytest==8.3.2
pytest-django==4.9.0
```

---

### **E. Makefile**

A Makefile automates repetitive commands, providing a professional workflow.

```makefile
.PHONY: up down logs web makemigrations migrate createsuperuser test clean

up:
	@echo "🚀 Starting stack (db + pgadmin + web)..."
	docker compose up -d --build

down:
	@echo "🧹 Stopping containers..."
	docker compose down

logs:
	docker compose logs -f

web:
	docker compose exec web bash

makemigrations:
	docker compose exec web python manage.py makemigrations

migrate:
	docker compose exec web python manage.py migrate

createsuperuser:
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web pytest -q

clean:
	@echo "🧽 Cleaning up Docker artifacts..."
	docker compose down -v --remove-orphans
	docker system prune -f
```

> 💡 *Students can now use* `make up` *to start the entire stack and* `make web` *to enter the container.*

---

### **Step 1 – Create the Django Project**

```bash
make web
django-admin startproject core .
python manage.py startapp events
```

Update **core/settings.py** with database settings using environment variables from `.env`.
Then migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **Step 2 – Model the Event System**

**events/models.py**

```python
from django.db import models

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=150)

class Registration(models.Model):
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("attendee", "event")
```

> 🧠 *Background:* You’re implementing a **many-to-many** relationship via a join table.
> Each Registration links one Attendee to one Event.

---

### **Step 3 – Create a Repository Layer (Managers)**

Django managers provide reusable query logic.

**events/repositories.py**

```python
from django.db import models
from .models import Attendee, Event, Registration

class AttendeeManager(models.Manager):
    def by_email(self, email):
        return self.filter(email__iexact=email)

class EventManager(models.Manager):
    def upcoming(self):
        return self.order_by("date")

class RegistrationManager(models.Manager):
    def for_attendee(self, attendee_id):
        return self.filter(attendee_id=attendee_id)
```

Attach to models (bottom of models.py):

```python
from .repositories import AttendeeManager, EventManager, RegistrationManager
Attendee.add_to_class("objects", AttendeeManager())
Event.add_to_class("objects", EventManager())
Registration.add_to_class("objects", RegistrationManager())
```

---

### **Step 4 – Service Layer with Transactions**

Encapsulate multi-step logic safely.

**events/services.py**

```python
from django.db import transaction, IntegrityError
from .models import Attendee, Event, Registration

class RegistrationService:
    @transaction.atomic
    def register(self, name, email, event_id):
        attendee, _ = Attendee.objects.get_or_create(email=email, defaults={"name": name})
        event = Event.objects.get(id=event_id)
        try:
            reg = Registration.objects.create(attendee=attendee, event=event)
        except IntegrityError:
            raise ValueError("Attendee already registered for this event.")
        return reg
```

> 💡 *Background:* `@transaction.atomic` ensures **all-or-nothing** execution — if anything fails, Django rolls back automatically.

---

### **Step 5 – Add Django REST Framework (API Layer)**

**events/serializers.py**

```python
from rest_framework import serializers
from .models import Attendee, Event, Registration

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"
```

**events/views.py**

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Event, Attendee, Registration
from .serializers import EventSerializer, AttendeeSerializer, RegistrationSerializer
from .services import RegistrationService

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    @action(detail=False, methods=["post"])
    def register(self, request):
        try:
            reg = RegistrationService().register(
                request.data["name"], request.data["email"], request.data["event_id"]
            )
            return Response({"id": reg.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
```

**core/urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from events.views import EventViewSet, RegistrationViewSet

router = DefaultRouter()
router.register("events", EventViewSet)
router.register("registrations", RegistrationViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
```

---

### **Step 6 – Test the DAL (pytest-django)**

**pytest.ini**

```ini
[pytest]
DJANGO_SETTINGS_MODULE = core.settings
python_files = tests.py test_*.py *_tests.py
```

**events/tests/test_services.py**

```python
import pytest
from datetime import date
from events.models import Event, Registration
from events.services import RegistrationService

pytestmark = pytest.mark.django_db

def test_register_success():
    event = Event.objects.create(title="Test", date=date.today(), location="Halifax")
    reg = RegistrationService().register("Alice", "alice@example.com", event.id)
    assert Registration.objects.count() == 1
    assert reg.attendee.email == "alice@example.com"
```

Run:

```bash
make test
```

---

## **5. Deliverables**

| Item           | Description                                                    |
| -------------- | -------------------------------------------------------------- |
| **Codebase**   | Django project (`core/`, `events/`), config files, Makefile    |
| **API Proof**  | Screenshot of `/api/events/` and `/api/registrations/register` |
| **Tests**      | pytest results (screenshot or logs)                            |
| **Reflection** | Written answers (Section 6)                                    |

---

## **6. Reflection Questions**

1. How does the Service Layer improve maintainability?
2. What’s the difference between ORM and raw SQL transactions?
3. Why use a Makefile in a development workflow?
4. How would you extend this API for front-end integration?
5. What part of this workflow best supports test-driven development (TDD)?

---

## **7. Evaluation Criteria**

| Category                 | Description                                | Weight |
| ------------------------ | ------------------------------------------ | ------ |
| **Implementation**       | Functional DAL with Managers, Service, API | 50%    |
| **Documentation**        | Clear instructions, screenshots, and logs  | 25%    |
| **Reflection & Testing** | Passing tests, critical insights           | 25%    |

