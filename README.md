# ELT Pipeline with dbt, PostgreSQL, and Docker

### 🚀 This project implements an ELT (Extract, Load, Transform) pipeline using:

- All services are run via Docker Compose
- dbt is configured to wait for the ELT script to complete before executing
- Models are stored in the `custom_postgres/models` directory 
- The pipeline is modular and can be scaled or integrated with orchestration tools like Airflow later

---

## 📦 Project Overview

### Goals

- Automate loading of data
- Automate transformation of data
- Ensure reproducible and isolated environment

### Architecture

The pipeline consists of the following services:

1. **PostgreSQL** as the data warehouse to store raw and transformed data
2. **Python** ELT scripts to load initial data into PostgreSQL
3. **dbt (Data Build Tool)** to transform and model the data
4. **Docker Compose** to orchestrate the stack

### Workflow

1. The PostgreSQL containers starts, create source DB and destination DB
2. The ELT script runs and populates destination DB with data from source DB
3. Once the ELT script completes successfully, dbt runs and transforms data into models

_To be continued ..._

---




