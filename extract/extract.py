import requests
from config import USER_AGENT, EDGAR_URL, YFINANCE_URL


class Request:
    def __init__(self):
        self.headers = None
        self.url = None

    def get_response(self, params):
        response = requests.get(url=self.url, params=params, headers=self.headers)
        response.raise_for_status()
        return response


class EdgarRequest(Request):
    def __init__(self):
        super().__init__()
        self.headers = {'User-Agent': USER_AGENT}
        self.url = EDGAR_URL

    def get_10k_filings_by_date(self, date):
        params = {
            'text': '10-K',
            'first': date,
            'last': date,
            'output': 'atom'
        }

        response = self.get_response(params)
        return response.text


class YahooFinanceRequest(Request):
    def __init__(self):
        super().__init__()
        self.headers = {'User-Agent': USER_AGENT}
        self.url = YFINANCE_URL

    def get_company_details(self, company_name):
        params = {"q": company_name, "quotes_count": 1, "country": "United States"}
        response = self.get_response(params)
        return response.json()
