from sqlalchemy import Column, String, Integer, Date, ForeignKey, Identity
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Company(Base):
    __tablename__ = 'companies'

    symbol = Column(String, primary_key=True)
    cik = Column(Integer)
    industry = Column(String)
    exchange = Column(String)
    longname = Column(String)
    shortname = Column(String)
    sector = Column(String)
    process_date = Column(Date)

    def __init__(self, symbol, cik, industry, exchange, longname, shortname, sector, process_date):
        self.symbol = symbol
        self.cik = cik
        self.industry = industry
        self.exchange = exchange
        self.longname = longname
        self.shortname = shortname
        self.sector = sector
        self.process_date = process_date

    def __repr__(self):
        return (f"Company(symbol={self.symbol}, name={self.shortname}, cik={self.cik}, "
                f"industry={self.industry}, exchange={self.exchange})")


class TenKFiling(Base):
    __tablename__ = 'tenk_filings'

    id = Column(Integer, Identity(start=1, cycle=True), primary_key=True)
    symbol = Column(String, ForeignKey('companies.symbol'), nullable=False)
    filing_type = Column(String)
    filing_url = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, symbol, filing_type, filing_url, date):
        super().__init__()
        self.symbol = symbol
        self.filing_type = filing_type
        self.filing_url = filing_url
        self.date = date

    def __repr__(self):
        return (f"<TenKFiling, symbol='{self.symbol}', filing_type='{self.filing_type}', "
                f"filing_url='{self.filing_url}', date='{self.date}')>")