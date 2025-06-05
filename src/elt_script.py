import subprocess
import time
import os
from dotenv import load_dotenv, find_dotenv
# Load environment variables from .env file
load_dotenv(find_dotenv())

def wait_for_postgres(host, max_retries=5, delay_sec=5):
    """
    Waits until PostgreSQL server is ready
    Ensure DB containers are up before continuing
    """
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            
            if "accepting connections" in result.stdout:
                print("Successfuly connected to Postgres !")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to Postgres : {e}")
            retries += 1
            print(f"Retrying in : {delay_sec} seconds, Attempt n° : {retries}, Max retries : {max_retries}.")
            time.sleep(delay_sec)
    print("Reached maximum retries. Exiting !")
    return False

# Exit script if the source DB is not ready
if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("START ELT SCRIPT ...")

# Load DB connection config from environment variables
source_config = {
    "dbname": os.getenv("POSTGRES_DB_SOURCE"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "source_postgres"
}

destination_config = {
    "dbname": os.getenv("POSTGRES_DB_DEST"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "destination_postgres"
}


# --- Step 1: Dump the entire source database to a SQL file ---
dump_command = [
    "pg_dump",
    "-h", source_config["host"],
    "-U", source_config["user"],
    "-d", source_config["dbname"],
    "-f", "data_dump.sql",
    "-w" # does not prompt for password each time
]
# Set password for pg_dump to use
subprocess_env = {"PGPASSWORD": source_config["password"]}
# Execute the dump
subprocess.run(dump_command, env=subprocess_env, check=True)

# --- Step 2: Load the dumped data into the destination database ---
load_command = [
    "psql",
    "-h", destination_config["host"],
    "-U", destination_config["user"],
    "-d", destination_config["dbname"],
    "-f", "data_dump.sql"
]
# Set password for psql to use
subprocess_env = {"PGPASSWORD": destination_config["password"]}
# Execute the load
subprocess.run(load_command, env=subprocess_env, check=True)

print("END ELT SCRIPT ...")