import os
import json
import requests
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='logs/errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def download_pdf(url, local_path):
    print(url)
    try:
        logging.info(f"Attempting to download {url}")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Check if the response content is not empty
        if not response.content:
            logging.error(f"Downloaded content is empty for {url}")
            return None

        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        logging.info(f"Successfully downloaded {url} to {local_path}")
        return local_path
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

def count_pdf_pages(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
    except PdfReadError as e:
        logging.error(f"PDF read error in {pdf_path}: {e}")
        return 0
    except Exception as e:
        logging.error(f"Error counting pages in {pdf_path}: {e}")
        return 0

def process_json_file(file_path):
    total_pages = 0
    comparison_date = datetime.strptime('2002-01-01', '%Y-%m-%d')
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                date = item['published_date']
                if date is not None:
                    date = datetime.strptime(date, '%Y-%m-%d')
                    if date < comparison_date:
                        break
                pdf_url = item['r2_url']
                local_pdf_path = f"{item['equity_ticker']}_{item['content_name']}.pdf"
                downloaded_path = download_pdf(pdf_url, local_pdf_path)
                print(downloaded_path)
                if downloaded_path:
                    total_pages += count_pdf_pages(downloaded_path)
                    os.remove(downloaded_path)  # Clean up downloaded file
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error in {file_path}: {e}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
    return total_pages

def update_results_json(results_file, equity, count):
    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)
    else:
        results = []

    results.append({'equity': equity, 'count': count})

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

def main(folder_path, results_file):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            equity = os.path.splitext(filename)[0]
            total_pages = process_json_file(file_path)
            update_results_json(results_file, equity, total_pages)

# Example usage
folder_path = 'Completed/US_Consumer_Discretionary'
results_file = 'Completed/us_Consumer_Discretionary.json'
main(folder_path, results_file)
download_pdf('https://pub-2c783279b61043e19fbdadd1bee5153a.r2.dev/OKTA/2024-12-03/Okta%2C%20Inc._2024-12-03_transcript/Okta%2C%20Inc._2024-12-03_transcript.pdf%5COkta%2C%20Inc._2024-12-03_transcript.pdf', 'sdsadsa.pdf')
