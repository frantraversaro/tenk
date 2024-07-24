# 10K Report Analysis Pipeline

This repository contains an ETL pipeline that ingests, cleans, and loads 10-K reports data from the Edgar API into Amazon Redshift. The data is going to be analyzed using a large language model to make investment decisions based on the report and the stock value/volume time series.

## Project Structure

```
10k/
├── dags/
│   ├── company_info_extraction_dag.py
│   ├── load_tables_dag.py
│   ├── tenk_extraction_dag.py
├── config/
│   ├── airflow.cfg
│   ├── webserver_config.py
│   ├── airflow-worker.pid
│   └── airflow-webserver.pid
├── logs/
│   └── (various log files)
├── src/
│   ├── extract/
│   │   ├── api_requests.py
│   │   ├── extract.py
│   │   ├── utils.py
│   │   └── __init__.py
│   ├── load/
│   │   ├── redshift_db/
│   │   │   ├── database.py
│   │   │   ├── handler.py
│   │   │   ├── models.py
│   │   │   └── __init__.py
│   │   ├── load.py
│   │   └── __init__.py
│   ├── constants.py
│   ├── io_utils.py
│   ├── requirements.txt
│   └── __init__.py
├── .env
├── .gitignore
├── docker-compose.yaml
├── Dockerfile
```

## Getting Started

### Prerequisites

Ensure you have the following installed on your local machine:

- Docker
- Docker Compose
- Python 3.9+
- Airflow
- Amazon Redshift

### Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/frantraversaro/tenk.git
    cd tenk
    ```

2. **Environment Variables:**

    Create a `.env` file in the root directory with the following variables:

    ```env
    AIRFLOW_UID=1000
    AWS_ACCESS_KEY_ID=<your_aws_access_key_id>
    AWS_SECRET_ACCESS_KEY=<your_aws_secret_access_key>
    REDSHIFT_HOST=<your_redshift_host>
    REDSHIFT_PORT=5439
    REDSHIFT_DB=<your_redshift_db>
    REDSHIFT_USER=<your_redshift_user>
    REDSHIFT_PASSWORD=<your_redshift_password>
    ```

3. **Docker Setup:**

    Build and start the containers using Docker Compose:

    ```sh
    docker-compose up --build
    ```

4. **Airflow Setup:**

    Initialize the Airflow database:

    ```sh
    docker-compose run airflow-init
    ```
   
    ```sh
    docker-compose up
    ```

    Access the Airflow webserver at [http://localhost:8080](http://localhost:8080) and login using the default credentials (`airflow/airflow`).

## Airflow DAGs

The following DAGs are defined in the `dags/` directory:

1. **tenk_extraction_dag.py:**
    - Ingests 10-K report data from the Edgar API.
    - Cleans and processes the data.
    - Loads the data into a local storage (later a datalake).

2. **company_info_extraction_dag.py:**
    - Extracts company information from the 10K reports.
    - Matches the CIK with the correct company stock symbol.
    - Loads the company details into a local storage (later a datalake).

3. **load_tables_dag.py:**
    - Loads processed data into the relevant Redshift tables.
    - Manages the ETL workflow and dependencies.

## Project Modules

- **src/extract/:** Contains modules for extracting 10-K report data from the Edgar API.
- **src/load/:** Contains modules for loading data into Redshift.
- **src/constants.py:** Defines constant values used across the project.
- **src/io_utils.py:** Utility functions for input/output operations.

## Best Practices

1. **Code Quality:**
    - Follow PEP 8 guidelines for Python code.
    - Use meaningful variable and function names.
    - Modularize the code for better maintainability.

2. **Version Control:**
    - Use `.gitignore` to exclude unnecessary files from version control.
    - Commit changes regularly with meaningful commit messages.

3. **Error Handling:**
    - Implement try-except blocks to handle exceptions gracefully.
    - Log errors using Airflow’s logging mechanism.

4. **Documentation:**
    - Document your code with docstrings.
    - Update this README file as the project evolves.

5. **Security:**
    - Do not hardcode sensitive information in the code.
    - Use environment variables for credentials and configuration.

