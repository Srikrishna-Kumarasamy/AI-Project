# Use a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy specific files (like requirements.txt) first
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Specify the default command
CMD ["python", "app.py"]
