# ELT Pipeline with dbt, PostgreSQL, Docker and Airflow

### 🚀 This project implements an ELT (Extract, Load, Transform) pipeline using:

- All services are run via Docker Compose
- dbt is configured to wait for the ELT script to complete before executing
- Models are stored in the `custom_postgres/models` directory 
- The pipeline is modular and can be scaled
- Airflow handles orchestration, scheduling, and monitoring of the ELT workflow

---

## 📦 Project Overview

### Goals

- Automate loading of data
- Automate transformation of data
- Ensure reproducible and isolated environment
- Orchestrate and schedule ELT tasks using Airflow
- Monitor and manage workflows through Airflow’s UI

### Architecture

The pipeline consists of the following services:

1. **PostgreSQL** as the data warehouse to store raw and transformed data
2. **Python** ELT scripts to load initial data into PostgreSQL
3. **dbt (Data Build Tool)** to transform and model the data
4. **Docker Compose** to define and run all services
5. **Apache Airflow** to orchestrate the ELT workflow  

### Workflow

1. The workflow begins by running *docker compose up init-airflow -d*, which initializes Airflow and sets up the metadata database and user
2. Then *docker compose up* starts all services, including PostgreSQL containers (source and destination) and Airflow components
3. Airflow detects that the databases are ready, then triggers the ELT script to extract data from the source DB and load it into the destination DB
4. Once the script ends successfully, Airflow triggers dbt, which transforms the loaded data into models stored in the destination DB

---




