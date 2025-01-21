# get the base image of python
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 5000
EXPOSE 5002

ENTRYPOINT ["python3"]
CMD ["run.py"]