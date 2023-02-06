FROM python:3.10-slim as builder

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN apt-get update && apt-get install -y git pip && pip install pipenv
RUN mkdir .venv && pipenv sync

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid 1000 --home-dir /home/app --create-home app

COPY --chown=app:app --from=builder /app /app

USER app

# Make port 5000 available to the world outside this container
EXPOSE 8888

# Run app.py when the container launches
CMD ["./run.sh"]
