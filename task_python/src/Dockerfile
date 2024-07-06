# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml ./

# Install Poetry and dependencies
RUN pip install poetry
RUN poetry install --no-root --only main

# Copy the rest of the application code to the container
COPY . .

RUN chmod +x /app/entrypoint.sh

# Set the command to run the shell script
CMD ["/app/entrypoint.sh"]