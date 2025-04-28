#!/usr/bin/env python
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

def write_json_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def fetch_sec_filings(symbol, api_key, filing_type):
    url = f"https://financialmodelingprep.com/api/v3/sec_filings/{symbol}?type={filing_type}&apikey={api_key}"
    return get_jsonparsed_data(url)

api_key = "P3jycMiIDB3fujYc6f2YpwfOBIzUSag1"
symbol = "CELH"
filing_types = ["10-K", "10-Q"]

all_filings = []
for filing_type in filing_types:
    filings = fetch_sec_filings(symbol, api_key, filing_type)
    all_filings.extend(filings)

write_json_to_file(all_filings, 'sec_filings.json')
print("SEC filings have been written to sec_filings.json")
