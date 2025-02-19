# Docker Learning Project

## Overview
This project demonstrates how to containerize a Python application using Docker. It includes a simple script (`Hello Docker.py`) and a `Dockerfile` to build and run the containerized application.

## Features
- Uses Docker to containerize a Python script.
- Includes a `.dockerignore` file to exclude unnecessary files.
- Configured with a `.gitignore` file to avoid committing unwanted files.
- Implements a structured `Dockerfile` for reproducible builds.

## Prerequisites
Ensure you have the following installed:
- Docker
- Python 3.x (for local testing before containerization)

## Setup and Usage

### Cloning the Repository
```bash
git clone https://github.com/Abhijeet-Real/Docker-Learn.git
cd docker-learning
```

### Building the Docker Image
```bash
docker build -t docker-learn .
```

### Running the Docker Container
```bash
docker run --rm docker-learn
```

## Project Structure
```
docker-learning/
│── .dockerignore         # Specifies files to ignore in Docker builds
│── .gitignore            # Specifies files to ignore in Git repository
│── Dockerfile            # Instructions to build the Docker image
│── Hello Docker.py       # Python script to be executed in the container
│── README.md             # Project documentation
```

## Expected Output
Running the container will execute `Hello Docker.py`, which may generate or process data using `pandas`, `numpy`, and `scipy.stats`.

## Future Improvements
- Add multi-stage builds for optimized Docker images.
- Use environment variables for configurable parameters.
- Extend the project to include additional Python scripts for learning purposes.

## License
This project is licensed under the MIT License.

## Author
Abhijeet 
abhijeet1472@gmail.com  
https://github.com/Abhijeet-Real