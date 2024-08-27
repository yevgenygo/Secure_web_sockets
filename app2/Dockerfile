# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current host dir into the container /app dir
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Remove unnecessary files
RUN rm -f /app/Dockerfile /app/requirements.txt

# Make port 3001 available to the world outside this container
EXPOSE 3001

# Run websocket_app.py when the container starts
CMD ["uvicorn", "websocket_app:app", "--host", "0.0.0.0", "--port", "3001", "--ssl-keyfile", "/app/server.key", "--ssl-certfile", "/app/server.crt"]
