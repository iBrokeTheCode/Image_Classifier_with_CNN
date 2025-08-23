---
title: Image Classifier With CNN
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 8501
tags:
  - streamlit
pinned: true
short_description: A CNN-based image classification with TensorFlow
license: mit
---

# 🖼️ Image Classification with ResNet50

## Table of Contents

1. [Project Description](#1-project-description)
2. [Methodology & Key Features](#2-methodology--key-features)
3. [Technology Stack](#3-technology-stack)
4. [Deployment Options](#4-deployment-options)
5. [Dataset](#5-dataset)

## 1. Project Description

This project implements an **image classification system** using a pre-trained **ResNet50 CNN** (trained on ImageNet with 1,000+ categories).

The repository includes **two versions**:

1. **Full Architecture (local, Dockerized):**

   - Built as a **multi-service ML system** with FastAPI (backend inference), Redis (queue/cache), and Streamlit (frontend).
   - Designed to demonstrate a scalable, production-like workflow.

2. **Lightweight Streamlit App (deployed):**
   - Adapted into a **single Streamlit app** for cost-effective deployment on **Hugging Face Spaces**.
   - Lets users upload an image and instantly see the **predicted category** with confidence.

This dual approach allows others to explore both a **realistic ML architecture** and a **lightweight, deployable demo**.

> [!IMPORTANT]
>
> - Check out the deployed app here: 👉️ [Image Classification App](https://huggingface.co/spaces/iBrokeTheCode/Image_Classifier_with_CNN) 👈️
> - Check out the source code for multi-service setup: 👉️ [Multi-Service - Source Code](https://huggingface.co/spaces/iBrokeTheCode/Image_Classifier_with_CNN/tree/main) 👈️
> - Check out the source code for lightweight Streamlit App: 👉️ [Lightweight App - Source Code](https://huggingface.co/spaces/iBrokeTheCode/Image_Classifier_with_CNN/tree/main/src) 👈️

![App Demo](./src/assets/app-demo.jpg)

## 2. Methodology & Key Features

- **Model:** ResNet50 (pre-trained on **ImageNet** with 1,000+ classes).
- **Pipeline:** Input images are resized, normalized, and passed to the model.
- **Output:** Top-1 prediction with **confidence score** is displayed.
- **Multi-service architecture:**
  - **FastAPI** serves inference requests.
  - **Redis** handles caching and task queueing.
  - **Streamlit** provides the interactive UI.
- **Lightweight deployment:** Direct **Streamlit-only** version for Hugging Face Spaces.

## 3. Technology Stack

This project was built using the following technologies:

**Deployment & Hosting:**

- [Docker](https://www.docker.com/) – containerization for the full architecture.
- [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces) – for lightweight deployment.
- [Streamlit](https://streamlit.io/) – interactive web app frontend.

**Backend & Infrastructure:**

- [FastAPI](https://fastapi.tiangolo.com/) – high-performance inference API.
- [Redis](https://redis.io/) – caching and message queue.

**Modeling & Training:**

- [TensorFlow / Keras](https://www.tensorflow.org/) – ResNet50 model (pre-trained on ImageNet).

**Development Tools:**

- [Ruff](https://github.com/charliermarsh/ruff) – Python linter and formatter.
- [uv](https://github.com/astral-sh/uv) – fast Python package installer and resolver.

## 4. Deployment Options

You can run this project in two ways:

### A. Run the Lightweight Version (Streamlit-only)

1. Clone the repo:

   ```bash
   git clone https://huggingface.co/spaces/iBrokeTheCode/Image_Classifier_with_CNN

   cd Image_Classifier_with_CNN
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   streamlit run src/streamlit_app.py
   ```

### B. Run the Full Architecture (Dockerized)

The repository also contains **Dockerfiles** for each service.

1. Clone the repo:

   ```bash
    git clone https://huggingface.co/spaces/iBrokeTheCode/Image_Classifier_with_CNN

   cd Image_Classifier_with_CNN
   ```

2. Pre-configure your environment variables:

   ```bash
   cp .env.original .env
   ```

3. Create a network for containers

   ```bash
   docker network create shared_network
   ```

4. Build and start all services:

   ```bash
   docker compose up --build -d

   # Stop services
   docker compose down
   ```

5. Populate the database

   ```bash
   cd api
   cp .env.original .env
   docker-compose up --build -d
   ```

6. Access the app at:

   ```
   http://localhost:9090
   ```

   Then use this credentials to pass the login:

   - Username: admin@example.com
   - Password: admin

7. Access the FastAPI app at:

   ```
   http://localhost:8000/docs
   ```

## 5. Dataset

This project uses the pre-training model ResNet50.

- **Model:** [ResNet50](https://www.tensorflow.org/api_docs/python/tf/keras/applications/ResNet50)
- **Classes:** 1,000+ categories (objects, animals, everyday items).
