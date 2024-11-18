# Use an official lightweight Python image.
FROM python:3.12-slim-bullseye AS base

# Set environment variables:
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Set the working directory inside the container
WORKDIR /myapp

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements to cache them in Docker layer
COPY ./requirements.txt /myapp/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of your application's code
COPY . /myapp

# Copy the startup script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the application as a non-root user for security
RUN useradd -m myuser

# Set correct permissions for app directory after copying files
RUN chown -R myuser:myuser /myapp

# Switch to the non-root user
USER myuser

# Expose port for the application
EXPOSE 8000

# Set the default command to start the application
CMD ["/start.sh"]
