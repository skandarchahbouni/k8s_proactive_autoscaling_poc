FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed dependencies specified in requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt


# Copy the current directory contents into the container at /app
COPY src .

# Make port 50051 available to the world outside this container
EXPOSE 50051

# Run app.py when the container launches
CMD ["python", "grpc_server.py"]