# Use a lightweight Python image (reduces size significantly)
FROM python:3.9.13-slim AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy only the dependencies file (requirements.txt) to the container
COPY requirements.txt .

# Install dependencies in a temporary layer to keep the final image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Use another lightweight Python image for the final container
FROM python:3.9.13-slim

# Set the working directory inside the final container
WORKDIR /app

# Copy the installed dependencies from the builder stage to the final image
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the rest of the project files into the final container
COPY . .

# Specify the command to run when the container starts
CMD ["python", "Hello Docker.py"]
