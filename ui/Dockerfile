from python:3.8.13 AS base

ENV PYTHONPATH=$PYTHONPATH:/src/

COPY ./requirements.txt /src/requirements.txt

WORKDIR /src

RUN pip install --upgrade pip && pip install -r requirements.txt

# 👇 Uncomment for DEPLOY / Comment for DevContainers
COPY ./ /src/ 

FROM base AS test
RUN ["python", "-m", "pytest", "-v", "tests"]

FROM base AS build
CMD streamlit run --server.port 9090 app/image_classifier_app.py