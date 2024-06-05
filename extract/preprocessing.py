import re

from bs4 import BeautifulSoup


# EDGAR response preprocessing

def extract_filing_data(entry):
    cik = None
    filing_url = None

    # Extract filing URL from the link tag
    link_tag = entry.find('link')
    if link_tag and 'href' in link_tag.attrs:
        filing_url = link_tag['href']

    # Extract CIK from the id tag or title tag
    id_tag = entry.find('id')
    title_tag = entry.find('title')

    if id_tag:
        cik_match = re.search(r'\b\d{10}\b', id_tag.get_text())
        if cik_match:
            cik = cik_match.group(0)

    if not cik and title_tag:
        cik_match = re.search(r'\b\d{10}\b', title_tag.get_text())
        if cik_match:
            cik = cik_match.group(0)

    filing_type, company_name = parse_filing_title(title_tag.get_text())
    return cik, company_name, filing_type, filing_url


def parse_filing_title(title):
    if "NT 10-K" in title:
        filing_type = "NT10K"
        company_name = title.split("NT 10-K - ")[1]
    elif "10-K" in title:
        filing_type = "10K"
        company_name = title.split("10-K - ")[1]
    else:
        # If neither "10-K" nor "NT 10-K" is found, return None for both filing type and company name
        filing_type = None
        company_name = None

    return filing_type, company_name


def enumerate_tags(content):
    soup = BeautifulSoup(content, 'lxml')
    entries = soup.find_all('entry')
    filings_data = []

    for entry in entries:
        cik, company_name, filing_type, filing_url = extract_filing_data(entry)
        if cik and filing_url:
            filings_data.append(
                {'cik': cik, 'company_name': company_name, 'filing_type': filing_type, 'filing_url': filing_url})
        else:
            print("Failed to extract CIK or Filing URL for an entry.")

    return filings_data


# YAHOO FINANCE response preprocessing
def extract_company_data(company_details):
    fetch_data = dict(
        symbol=[],
        industry=[],
        exchange=[],
        longname=[],
        shortname=[],
        sector=[])

    for quote in company_details['quotes']:
        exchange = quote.get('exchDisp')
        longname = quote.get('longname')
        exchange_filter = bool(exchange) and (('nyse' in exchange.lower()) or ('nasdaq' in exchange.lower()))
        longname_filter = ('equity' not in longname.lower() if longname else True)

        if exchange_filter and longname_filter:
            fetch_data['symbol'].append(quote.get('symbol'))
            fetch_data['industry'].append(quote.get('industry'))
            fetch_data['exchange'].append(exchange)
            fetch_data['longname'].append(longname)
            fetch_data['shortname'].append(quote.get('shortname'))
            fetch_data['sector'].append(quote.get('sector'))

    output = {key: [v for v in set(value) if v is not None] for key, value in fetch_data.items()}

    for key, value in output.items():
        if key == "symbol":
            symbol = min(value, key=len, default=None)
            if symbol is None:
                return None
            else:
                output[key] =symbol
        else:
            output[key] = value[0] if value else "Unknown"
    return output
