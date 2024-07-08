# Use the official Python image as a base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the pyproject.toml and poetry.lock files to the container
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI application with uvicorn
CMD ["poetry", "run", "uvicorn", "imtiaz_mart.main:app", "--host", "127.0.0.1", "--port", "8000"]
