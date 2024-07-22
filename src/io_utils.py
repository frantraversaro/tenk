import logging
import os
from datetime import date

import pandas as pd

from src.constants import OUTPUT_PATH


def save_to_datalake(data: pd.DataFrame, key: str, bucket: str = OUTPUT_PATH):
    """
    Save data to S3 (For now is implemented to save in airflow output folder)
    :param key: the folder
    :param data: the data to save
    :param bucket: the main folder (s3 bucket)
    :return: None
    """
    path = os.path.join(bucket, key)
    if not os.path.exists(path):
        os.makedirs(path)
    data.to_csv(os.path.join(path, 'data.csv'), index=False)


def load_from_datalake(key: str, bucket: str = OUTPUT_PATH) -> pd.DataFrame:
    """
    Save data to S3 (For now is implemented to save in airflow output folder)
    :param key: the folder
    :param bucket: the main folder (s3 bucket)
    :return: None
    """
    filename = os.path.join(bucket, key, 'data.csv')
    logging.info(f"Reading data from {filename}")
    data = pd.read_csv(filename)
    return data


if __name__ == '__main__':
    date_str = date.today().strftime('%Y%m%d')
    key = f'tenk_extraction/{date_str}/'
    df = load_from_datalake(key=key)
    print('Done')