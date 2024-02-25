# Use Alpine Linux as a base image
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLAG=SparkCTF{inspired_by_CVE-2023-42802_15967471a9d70048d31e0f17651c7b67}

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project directory into the container at /app
COPY . /app/

# Expose port 5000 to allow communication to/from the Flask application
EXPOSE 5000

# Define environment variables for Flask
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0

# Command to run the Flask application
CMD ["flask", "run"]
