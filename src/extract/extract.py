from datetime import date

import pandas as pd

from src.extract.api_requests import EdgarRequest, YahooFinanceRequest
from src.extract.utils import extract_filing_data, extract_companies_details


def download_10k(dt: date):
    """
    Download 10k xml
    :param dt: the date of interest
    :return: a xml string
    """
    str_date = dt.strftime('%Y-%m-%d')
    edgar_request = EdgarRequest()
    filings_xml = edgar_request.get_10k_filings_by_date(str_date)
    return filings_xml


def extract_10K(xml: str):
    """
    Extract 10k filing data from downloaded xml
    :param xml:
    :return:
    """
    filings_data = extract_filing_data(xml)
    return filings_data


def get_companies_details(filings_data: pd.DataFrame):
    """
    Extract companies details present in filings data dataframe
    :param filings_data: a dataframe with 10K filings
    :return: the list of company details dict
    """
    yahoo_request = YahooFinanceRequest()
    companies_details = extract_companies_details(filings_data, yahoo_request)
    return companies_details


if __name__ == '__main__':
    """
    Extract 10k filings
    """
    xml = download_10k(date.today())
    data = extract_10K(xml)
    companies = get_companies_details(data)
    print(companies)


