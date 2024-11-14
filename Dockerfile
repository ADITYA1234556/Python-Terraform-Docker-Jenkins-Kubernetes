# Use the official Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the app code into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port Flask runs on
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run"]
