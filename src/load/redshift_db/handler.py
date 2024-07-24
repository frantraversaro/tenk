from src.load.redshift_db.database import create_tables
from src.load.redshift_db.models import Company, TenKFiling
from sqlalchemy import func


def add_company(symbol, cik, industry, exchange, longname, shortname, sector, process_date, session):
    company = session.query(Company).filter_by(symbol=symbol).one_or_none()

    if company is None:
        new_company = Company(symbol, cik, industry, exchange, longname, shortname, sector, process_date)
        session.add(new_company)
        print(f"Created company: {new_company}")
    else:
        print(f"Company {symbol} already exists in table: {company}")


def add_tenk_filing(symbol, filing_type, filing_url, filing_date, session):
    tenk = session.query(TenKFiling).filter_by(symbol=symbol, date=filing_date, filing_type=filing_type).one_or_none()

    if tenk is None:
        tid = (session.query(func.max(TenKFiling.tid)).scalar() or 0) + 1
        new_tenk = TenKFiling(tid, symbol, filing_type, filing_url, filing_date)
        session.add(new_tenk)
        print(f"Created 10K filing: {new_tenk}")
    else:
        print(f"10K filing {symbol} of type {filing_type} on date {filing_date} already exists in table: {tenk}")

