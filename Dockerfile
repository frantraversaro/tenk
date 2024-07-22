FROM apache/airflow:2.3.3

# Copy custom code
COPY src /opt/airflow/src
COPY .env /opt/airflow/.env
# Install dependencies from requirements.txt
RUN pip install python-decouple

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"
