# Use Python 3.9.13 as the base image
FROM python:3.9.13

# Set the working directory inside the container
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Create a virtual environment inside the container
RUN python -m venv .venv

# Activate the virtual environment and install dependencies
RUN .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt

# Ensure the virtual environment is used when running the container
ENV PATH="/app/.venv/bin:$PATH"

# Run the Python script inside the virtual environment
CMD ["python", "Hello Docker.py"]
