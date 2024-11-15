# Use an official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies for mysqlclient
#RUN apt-get update && \
#    apt-get install -y default-libmysqlclient-dev build-essential mariadb-client && \
#    rm -rf /var/lib/apt/lists/* \

RUN apt-get update && \
    apt-get install -y wget gnupg lsb-release && \
    # Add MySQL APT GPG key
    wget https://dev.mysql.com/get/mysql-apt-config_0.8.17-1_all.deb && \
    wget https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-apt-config_0.8.17-1_all.deb && \
    dpkg -i mysql-apt-config_0.8.17-1_all.deb && \
    apt-get update && \
    apt-get install -y mysql-client && \
    rm -rf /var/lib/apt/lists/*

#RUN apt-get update && \
#    apt-get install -y default-libmysqlclient-dev build-essential && \
#    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY wait.sh /wait.sh
RUN chmod +x /wait.sh

# Copy the rest of the application code into the container
COPY main.py .

# Set environment variables for Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=development

# Expose the port Flask will run on
EXPOSE 5000

# Run the application
#CMD ["flask", "run", "--host=0.0.0.0"]

CMD ["/wait.sh", "mysql-service:3306", "--", "flask", "run", "--host=0.0.0.0", "--port=5000"]
