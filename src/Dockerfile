# Python lightweight image
FROM python:3.12.1-slim
 
# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set working directory
WORKDIR /app

# Copy requirements.txt to container and install python dependencies
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ETL script to container
COPY src/elt_script.py .

# Run command when the container starts
CMD ["python", "elt_script.py"]