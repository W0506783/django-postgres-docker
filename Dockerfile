# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your project code
COPY . /app/

# Set the default command (overridden by docker-compose.yml)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
