from src.load.redshift_db.database import get_session
from src.load.redshift_db.handler import add_company, add_tenk_filing

def load_companies(companies_detail_df, process_date):
    session = get_session()
    try:
        for _, company_data in companies_detail_df.iterrows():
            add_company(
                symbol=company_data['symbol'],
                cik=int(company_data['cik']),
                industry=company_data['industry'],
                exchange=company_data['exchange'],
                longname=company_data['longname'],
                shortname=company_data['shortname'],
                sector=company_data['sector'],
                process_date=process_date,
                session=session
            )
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def load_filings(filings_data):
    session = get_session()
    try:
        for _, filing_data in filings_data.iterrows():
            add_tenk_filing(
                symbol=filing_data['symbol'],
                filing_type=filing_data['filing_type'],
                filing_url=filing_data['filing_url'],
                filing_date=filing_data['filing_date'],
                session=session
            )
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()
