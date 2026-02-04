# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the source code into the container
COPY . .

# Command to run the application
CMD ["python", "app.py"]
