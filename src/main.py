from datetime import date

from src.db.database import create_tables
from src.extract.preprocessing import enumerate_tags, extract_company_data
from src.extract.requests import EdgarRequest, YahooFinanceRequest
from src.db.handler import create_company, create_tenk_filing

def run():
    create_tables()
    # Example usage
    current_date = date.today()
    str_date = current_date.strftime('%Y-%m-%d')
    
    edgar_request = EdgarRequest()
    yahoo_request = YahooFinanceRequest()

    filings = edgar_request.get_10k_filings_by_date(str_date)
    filings_data = enumerate_tags(filings)
    for f in filings_data:
        cik = int(f['cik'])
        company_name = f['company_name']
        filing_type = f['filing_type']
        filing_url = f['filing_url']
        
        company_details = yahoo_request.get_company_details(company_name)
        company_data = extract_company_data(company_details)

        if company_data is not None:
            symbol = company_data['symbol']
            industry = company_data['industry']
            exchange = company_data['exchange']
            longname = company_data['longname']
            shortname = company_data['shortname']
            sector = company_data['sector']

            create_company(symbol, cik, industry, exchange, longname, shortname, sector)
            create_tenk_filing(symbol, filing_type, filing_url, current_date)