# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install git and make
RUN apt-get update && apt-get install -y git make

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application into the container
COPY . /app/

ENV PYTHONPATH=/app

# Make port 80 available to the world outside this container
EXPOSE 80