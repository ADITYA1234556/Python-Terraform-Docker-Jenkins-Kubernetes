# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Expose the port Flask will run on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
