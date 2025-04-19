import os
import json
import logging
import requests
from sec_api import QueryApi
from urllib.parse import urlparse
from argparse import ArgumentParser
from utils.upload_to_r2 import upload_to_r2

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
quarter_cycle = [4, 3, 2, 1]  # Order of quarters (Q4 -> Q3 -> Q2 -> Q1)
quarter_index = 0
latest_year = None

def find_first_10k_index(filings):
    for index in range(len(filings)):
        if filings[index]['formType'] == '10-K':
            return index, int(filings[index].get("periodOfReport", "")[:4])
    return -1  # Return -1 if no 10-K form type is found

def map_value(value):
    if value == 0:
        return 4
    elif value == 1:
        return 3
    elif value == 2:
        return 2
    elif value == 3:
        return 1
    else:
        return 0  # Return None or raise an error for unexpected values

fils = response.get("filings", [])
ind, latest_year = find_first_10k_index(fils)
quarter_index = map_value(ind)
if ind != 0:
    latest_year = latest_year + 1


for filing in response.get("filings", []):
    try:
        form_type = filing.get("formType")
        file_url = filing.get("linkToFilingDetails")
        filed_at = filing.get("filedAt", "")[:10]
        period_of_report = filing.get("periodOfReport", "")[:4]  # Get year from 'YYYY-MM-DD'

        if not file_url or form_type not in ["10-K", "10-Q"]:
            continue

        if form_type == "10-K":
            content_type = "annual_report"
        else:
            content_type = "quarterly_report"

        fiscal_quarter = quarter_cycle[quarter_index]

        if fiscal_quarter == 4:
            latest_year = int(period_of_report)
            fiscal_year = latest_year
        else:
            fiscal_year = latest_year

        content_name = f"{EQUITY_TICKER} Q{fiscal_quarter} {fiscal_year} {content_type}"
        logging.info(f"Processing {form_type} filing for Q{fiscal_quarter} {fiscal_year}")

        file_path = download_sec_pdf(API_KEY, file_url)
        if file_path:
            r2_key = f"{EQUITY_TICKER}/{filed_at}/{os.path.basename(file_url)}"
            r2_url = upload_to_r2(file_path, r2_key, False)

            extracted_filings.append({
                "equity_ticker": EQUITY_TICKER,
                "geography": "US",
                "content_name": content_name,
                "file_type": "pdf",
                "content_type": content_type,
                "published_date": filed_at,
                "fiscal_date": filing.get("periodOfReport"),
                "fiscal_year": fiscal_year,
                "fiscal_quarter": fiscal_quarter,
                "r2_url": r2_url,
                "periodicity": "periodic",
            })

            logging.info(f"Uploaded to R2: {r2_url}")
        else:
            logging.warning(f"Skipping upload for failed PDF: {file_url}")

        # Move to next quarter (wrap after 4)
        quarter_index = (quarter_index + 1) % len(quarter_cycle)

    except Exception as e:
        logging.exception(f"Error processing filing: {filing}")

# --- Save Output ---
output_filename = f"JSONS/{EQUITY_TICKER}_sec_filings.json"
try:
    os.makedirs("JSONS", exist_ok=True)
    with open(output_filename, "w") as f:
        json.dump(extracted_filings, f, indent=2)
    logging.info(f"Saved extracted filings to {output_filename}")
except Exception as e:
    logging.exception(f"Failed to write output JSON file: {e}")
