FROM apache/airflow:2.3.3

# Copy custom code
COPY src /opt/airflow/src

# Install any additional dependencies if needed
# RUN pip install some-package

# Set the PYTHONPATH to include the src directory
ENV PYTHONPATH="/opt/airflow:${PYTHONPATH}"
