# Use a specific version of python:3.11-slim as the base image. 
# I'm using python:3.11 for compatibility with crewAI
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies and clean up apt cache in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the source dir
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose the port that Streamlit will run on
EXPOSE 8501

# Add a health check to ensure the container is running as expected
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Set the entrypoint to run the Streamlit application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]