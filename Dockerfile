# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install the application and its dependencies
RUN pip install --no-cache-dir -e .

# Expose the port that Streamlit runs on
EXPOSE 8501

# ENCRYPTION_KEY must be supplied at runtime (e.g. via --env-file or docker-compose).
# The app refuses to start without a real, non-default value — see config/settings.py.

# Run streamlit when the container launches
ENTRYPOINT ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
