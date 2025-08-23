# Lessons Learned

## Table of Contents

1. [Docker](#1-docker)
2. [Dev Containers](#2-dev-containers)
3. [Redis](#3-redis)
4. [Postgres](#4-postgres)
5. [Unit Tests](#5-unit-tests)
6. [Locust](#6-locust)
7. [AWS](#7-aws)
8. [GitHub Actions](#8-github-actions)
9. [Streamlit](#9-streamlit)

## 1. Docker

- Install [Docker](https://docs.docker.com/engine/install/)
- Some basic Docker commands:

  ```bash
  # List all containers
  docker ps

  # List all images
  docker images

  # Remove resources
  docker rmi $(docker images -q)
  docker rm $(docker ps -aq)

  # Network
  docker network ls
  docker network rm <network_id>

  # Volumes
  docker volume ls
  docker volume rm <volume_id>

  # Build an image
  docker build -t <image_name> .

  # Build a test image (target)
  docker build -t ui_test --progress=plain --target test .

  # Run a container
  docker run -p <port>:<port> -d <image_name>
  ```

### 1.1 Dockerfile

- A basic example of a Dockerfile

  ```Dockerfile
  # Base image
  FROM python:3.9

  # Set working directory
  WORKDIR /app

  # Copy files
  COPY . /app

  # Install dependencies (during build time)
  RUN pip install -r requirements.txt

  # Run the app (after installing dependencies)
  CMD ["python", "main.py"]
  ```

### 1.2 Docker Compose

- A basic example of a Docker Compose file running microservices:

  ```yml
  services:
    api: # Name of the service
      build: # Build the image
        context: ./ui
        target: build # Target
      ports: # Ports
        - "8000:8000"
      environment: # Env variables
        POSTGRES_DB: $POSTGRES_DB
        POSTGRES_USER: $POSTGRES_USER
        POSTGRES_PASSWORD: $POSTGRES_PASSWORD
        DATABASE_HOST: $DATABASE_HOST
      depends_on: # Dependencies
        - redis
        - db
      networks: # Network
        - shared_network
      volumes: # Volumes
        - ./uploads:/src/uploads
    db: # Another service
      image: postgres:13-alpine
      volumes: # Volumes
        - postgres_data:/var/lib/postgresql/data
    redis: # Another service
      image: redis:6.2.6
      networks:
        - shared_network
  networks:
    shared_network:
  volumes:
    postgres_data:
  ```

## 2. Dev Containers

- Install [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension
- Create a `.devcontainer` folder
- Create folders for each service you want to develop (api, model, ui, etc.)
- Create a `devcontainer.json` file
- Optionally you can create Dockerfiles or Docker Compose files for each service

  ```json
  {
    "name": "ML Project - API",
    "dockerComposeFile": "../../docker-compose-dev.yml",
    "service": "api",
    "workspaceFolder": "/src",
    "customizations": {
      "vscode": {
        "extensions": ["ms-python.python"]
      }
    },
    "shutdownAction": "none"
  }
  ```

  - Note: Don't use `COPY` command inside your Dockerfile, use `volumes` in your Docker Compose file to edit files inside the container. (for development stage)

  ```yml
  # ...
  volumes:
    - ./ui:/src:cached
  # ...
  ```

  - Run the dev container by selecting `devcontainer: Reopen in Container` option (`ctrl + shift + P`)

## 3. Redis

- To connect to a Redis instance by terminal you can use the following command:

  ```bash
  redis-cli
  ```

- Some basics commands:

  ```bash
  # Set a key
  SET key value

  # Get a key
  GET key

  # Delete a key
  DEL key

  # List all keys
  KEYS *
  ```

  Review [Redis Commands Cheat Sheet](https://redis.io/learn/howtos/quick-start/cheat-sheet) for more commands.

- Monitor the Redis instance with the command:

  ```bash
  redis-cli monitor
  ```

## 4. Postgres

- To connect to a Postgres instance by terminal you can use the following command:

  ```bash
  psql -U <username> -p 5432 -d <database_name>
  ```

- Can also use a Postgres GUI client, like DBeaver. So you can use the connection values from the Docker Compose file.

- Some basics commands are:

  ```bash
  # List all databases
  \l

  # Create a database
  CREATE DATABASE <database_name>;

  # List all tables
  \dt

  # Exit
  \q
  ```

## 5. Unit Tests

### 5.1 Unittest

- To run unit tests you can use the following commands:

  ```bash
  # Run test file
  python3 -m unittest -vvv tests.test_model

  # Run an individual test
  python -m unittest -vvv tests.test_image_classifier_app.TestMLService.test_login_failure
  ```

- Additionally can run test from the python module:

  ```py
  if __name__ == "__main__":
    unittest.main(verbosity=2)
  ```

  And then run the module

  ```bash
  python tests/test_image_classifier_app.py
  ```

### 5.2 Pytest

- To run unit tests you can use the following commands:

  ```bash
  # Run test file
  pytest -v -s tests/test_model.py

  # Run an individual test
  pytest -v -s tests/test_image_classifier_app.py::TestMLService::test_login_failure
  ```

## 6. Locust

- Install [locust](https://docs.locust.io/en/stable/quickstart.html#locust-s-web-interface)

  ```bash
  uv add locust
  ```

- Create a folder `stress_test` and `locustfile.py` file

  ```py
  # Basic example
  from locust import HttpUser, task

  class HelloWorldUser(HttpUser):
      @task
      def hello_world(self):
          self.client.get("/hello")
          self.client.get("/world")
  ```

- Run `locust -f stress_test/locustfile.py`
- Open `http://127.0.0.1:8089`
- Start a load test and fill the number of users/ramp up
- Add the host, for example `http://localhost:8000`
- Start the load test
- Review the results, stats and charts

## 7. AWS

- Download the `epm` file from your AWS account
- Give read permissions to the file with:
  ```bash
  chmod 400 file.epm
  ```
- Connect it via ssh
  ```bash
  ssh -i file.epm <ec2_user>@<public_ip>
  ```
- To copy files from local host to remote host:

  ```bash
  scp -i file.epm -r <local_path> <ec2_user>@<public_ip>: # Default home
  scp -i file.epm -r <local_path> <ec2_user>@<public_ip>:<remote_path>
  ```

- Create a tunnel to the remote host:

  ```bash
  ssh -L <local_port>:<remote_host>:<remote_port> -i file.epm <ec2_user>@<public_ip>
  ```

## 8. GitHub Actions

GitHub Actions is a **CI/CD (Continuous Integration and Continuous Deployment)** tool built into GitHub that allows you to **automate workflows** directly from your repository. With Actions, you can run tests, build your code, deploy applications, and perform other automated tasks whenever certain events occur (like pushing code, creating pull requests, or publishing releases).

Key points:

- **Event-driven**: Workflows run based on triggers like `push`, `pull_request`, or scheduled cron jobs.
- **YAML-based**: Workflows are defined in `.github/workflows/` using YAML syntax.
- **Cross-platform**: Supports Linux, Windows, and macOS runners.
- **Marketplace**: Offers reusable actions to speed up development.

---

### **Basic Example: CI Workflow for Python Project**

```yaml
# File: .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run tests
        run: |
          pytest
```

**What this does:**

- Runs when you **push or create a pull request** to the `main` branch.
- Uses **Ubuntu** as the environment.
- Sets up **Python 3.10**, installs dependencies, and runs **pytest** for tests.

## 9. Streamlit

To fix **telemetry issues** and **403 errors on file uploads** during deployment (Docker/Hugging Face Spaces)., configure Streamlit with a `config.toml` in `/app/.streamlit/`:

```toml
[browser]
gatherUsageStats = false

[server]
enableCORS = false
enableXsrfProtection = false
```

In Dockerfile:

```dockerfile
RUN mkdir -p /app/.streamlit /app/tmp
COPY .streamlit/ /app/.streamlit/
```

Or generate the same configuration in build stage:

```dockerfile
RUN mkdir -p /app/.streamlit \
    && echo "[browser]\n" \
           "gatherUsageStats = false\n\n" \
           "[server]\n" \
           "enableCORS = false\n" \
           "enableXsrfProtection = false\n" \
           > /app/.streamlit/config.toml
```
