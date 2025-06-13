from datetime import datetime
from airflow import DAG
from docker.types import Mount
from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
import subprocess

# Default parameters for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
}

# Run the ELT script
def run_script():
    script_path = "/opt/airflow/src/elt_script.py"

    result = subprocess.run(["python", script_path], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Script failed ! Error : {result.stderr}")
    else:
        print(result.stdout)

# The DAG
dag = DAG(dag_id="elt_and_dbt", description="ELT workflow with dbt", default_args=default_args, start_date=datetime(2025, 6, 10), catchup=False)

# First task : run the ELT script
task_1 = PythonOperator(task_id="run_elt_script", python_callable=run_script, dag=dag)

# Second task: run dbt in a container
task_2 = DockerOperator(
    task_id="run_dbt", 
    image="ghcr.io/dbt-labs/dbt-postgres:1.8.2@sha256:95d7bb3a14fc9e1b7122e1389e80c8710c87da7ac57b6ccc1ec4eae3b9bbd2ac",
    command=["run", "--profiles-dir", "/root", "--project-dir", "/opt/dbt"],
    auto_remove=True,
    docker_url="unix://var/run/docker.sock",
    network_mode="elt_elt_network",
    mounts=[
        Mount(source="/Users/sarahrouini/maxplotlib/ELT/custom_postgres",target="/opt/dbt", type="bind"),
        Mount(source="/Users/sarahrouini/.dbt", target="/root/", type="bind")
    ],
    dag=dag)

# Order of execution
task_1 >> task_2
