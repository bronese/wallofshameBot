# Use the official Python image as the base image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
ADD requirements.txt /app/requirements.txt

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
ADD . /app

# Run the script when the container starts
CMD ["python", "main.py"]