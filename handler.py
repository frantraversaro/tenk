from datetime import date
from database import get_session, create_tables
from models import Company, TenKFiling
from sqlalchemy import func

def create_company(symbol, cik, industry, exchange, longname, shortname, sector):
    session = get_session()
    company = session.query(Company).filter_by(symbol=symbol).one_or_none()

    try:
        if company is None:
            process_date = date.today()
            new_company = Company(symbol, cik, industry, exchange, longname, shortname, sector, process_date)
            session.add(new_company)
            session.commit()
            print(f"Created company: {new_company}")
        else:
            print(f"Company {symbol} already exists in table: {company}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()


def create_tenk_filing(symbol, filing_type, filing_url, filing_date):
    session = get_session()
    tenk = session.query(TenKFiling).filter_by(symbol=symbol, date=filing_date, filing_type=filing_type).one_or_none()

    try:
        if tenk is None:
            tid = (session.query(func.max(TenKFiling.tid)).scalar() or 0) + 1
            new_tenk = TenKFiling(tid, symbol, filing_type, filing_url, filing_date)
            session.add(new_tenk)
            session.commit()
            print(f"Created 10K filing: {new_tenk}")
        else:
            print(f"10K filing {symbol} of type {filing_type} on date {filing_date} already exists in table: {tenk}")
    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")
    finally:
        session.close()



# Example usage
if __name__ == "__main__":
    create_tables()
    create_company("AAPL", 123456, "Technology", "NASDAQ", "Apple Inc.", "Apple", "Consumer Electronics")
    #create_tenk_filing("AAPL", "10K", "http://example.com/filing", date(2023, 5, 31))
