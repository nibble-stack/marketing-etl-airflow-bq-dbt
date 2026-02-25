FROM apache/airflow:3.1.7-python3.11

USER root

# Optional system deps
# RUN apt-get update && apt-get install -y build-essential

USER airflow

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /requirements.txt
