# Use the latest Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only the Poetry files to leverage Docker caching for dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies with Poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code into the container
COPY . /app

# Make port 4008 available to the world outside this container
EXPOSE 4008

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4008", "--reload"]
