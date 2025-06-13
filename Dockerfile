# airflow image
FROM apache/airflow:2.7.1

# Install docker provider so Airflow can run containers as tasks
RUN pip install apache-airflow-providers-docker