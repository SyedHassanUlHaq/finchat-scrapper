import os
import json
import logging
import requests
from sec_api import QueryApi
from weasyprint import HTML
from urllib.parse import urlparse
from datetime import datetime
from argparse import ArgumentParser
from utils.upload_to_r2 import upload_to_r2
from utils.get_closest_date import find_closest_date
from utils.get_quarter_and_year import get_quarter_and_year

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("sec_pdf_scraper.log"),
        logging.StreamHandler()
    ]
)

# --- Argument Parsing ---
parser = ArgumentParser(description="Scrape filings from SEC API")
parser.add_argument("ticker", type=str, help="Equity ticker to scrape filings for")
parser.add_argument("json_path", type=str, help="Path to the JSON file containing dates")
args = parser.parse_args()

EQUITY_TICKER = args.ticker
API_KEY = "22d149980740890dce43a4e05c91d4923b20c6ae90cc9bb07a6fe28720cae6a5"

# --- PDF Download Function ---
def download_sec_pdf(api_token, filing_url):
    try:
        os.makedirs("downloads", exist_ok=True)
        parsed_url = urlparse(filing_url)
        filename = os.path.basename(parsed_url.path)
        pdf_filename = os.path.splitext(filename)[0] + ".pdf"
        pdf_path = os.path.join("downloads", pdf_filename)

        api_endpoint = "https://api.sec-api.io/filing-reader"
        query_params = {"token": api_token, "url": filing_url}
        logging.info(f"Requesting PDF for: {filing_url}")

        response = requests.get(api_endpoint, params=query_params, stream=True)

        if response.status_code == 200 and response.headers['Content-Type'] == 'application/pdf':
            with open(pdf_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            logging.info(f"PDF saved to {pdf_path}")
            return pdf_path
        else:
            logging.error(f"Failed to download PDF | Status: {response.status_code} | URL: {filing_url}")
            logging.debug(f"Response content: {response.text}")
            return None
    except Exception as e:
        logging.exception(f"Exception during PDF download: {e}")
        return None

# --- Initialize Query API ---
queryApi = QueryApi(api_key=API_KEY)
search_query = f'ticker:{EQUITY_TICKER} AND (formType:"10-K" OR formType:"10-Q")'
parameters = {
    "query": search_query,
    "from": "0",
    "sort": [{"filedAt": {"order": "desc"}}],
}

logging.info(f"Fetching filings for ticker: {EQUITY_TICKER}")
response = queryApi.get_filings(parameters)

# --- Process Filings ---
extracted_filings = []

for filing in response.get("filings", []):
    try:
        form_type = filing.get("formType")
        file_url = filing.get("linkToFilingDetails")
        filed_at = filing.get("filedAt", "")[:10]
        period_of_report = filing.get("periodOfReport")

        if form_type == "10-K":
            content_type = "annual_report"
        elif form_type == "10-Q":
            content_type = "quarterly_report"
        else:
            content_type = None

        closest_date = find_closest_date(args.json_path, period_of_report)
        fiscal_year, fiscal_quarter = get_quarter_and_year(closest_date)

        logging.info(f"Processing {form_type} filing from {filed_at}")
        content_name = EQUITY_TICKER + f" Q{fiscal_quarter}" + f" {fiscal_year} " + content_type
        file_path = download_sec_pdf(API_KEY, file_url)
        if file_path:
            r2_key = f"{EQUITY_TICKER}/{filed_at}/{os.path.basename(file_url)}"
            r2_url = upload_to_r2(file_path, r2_key, True)
            extracted_filings.append({
                "equity_ticker": EQUITY_TICKER,
                "geography": "US",
                "content_name": content_name,
                "file_type": "pdf",
                "content_type": content_type,
                "published_date": filed_at,
                "fiscal_date": period_of_report,
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter if content_type == "quarterly_report" else 4,
                "r2_url": r2_url,
                "periodicity": "periodic",
            })
            
            print(extracted_filings)
            logging.info(f"Uploaded to R2: {r2_url}")
        else:
            logging.warning(f"Skipping upload for failed PDF: {file_url}")
    except Exception as e:
        logging.exception(f"Error processing filing: {filing}")

# --- Summary Output ---
logging.info(f"\nExtracted {len(extracted_filings)} 10-K/10-Q filings for {EQUITY_TICKER}.")
for filing in extracted_filings[:5]:
    logging.debug(json.dumps(filing, indent=2))
    
output_filename = f"{EQUITY_TICKER}_sec_filings.json"
try:
    with open(output_filename, "w") as f:
        json.dump(extracted_filings, f, indent=2)
    logging.info(f"Saved extracted filings to {output_filename}")
except Exception as e:
    logging.exception(f"Failed to write output JSON file: {e}")
