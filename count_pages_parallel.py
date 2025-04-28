import os
import json
import requests
from PyPDF2 import PdfReader
import logging
from datetime import datetime
from multiprocessing import Pool, cpu_count

# Configure logging
logging.basicConfig(filename='logs/errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def download_pdf(url, local_path):
    print(url)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Check if the response content is not empty
        if not response.content:
            logging.error(f"Downloaded content is empty for {url}")
            return None

        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return local_path
    except requests.RequestException as e:
        logging.error(f"Error downloading {url}: {e}")
        return None

def count_pdf_pages(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            return len(reader.pages)
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
                try:
                    date = item['published_date']
                    if date is not None:
                        date = datetime.strptime(date, '%Y-%m-%d')
                        if date < comparison_date:
                            break
                    pdf_url = item['r2_url']
                    local_pdf_path = f"{item['equity_ticker']}_{item['content_name']}.pdf"
                    downloaded_path = download_pdf(pdf_url, local_pdf_path)
                    if downloaded_path:
                        total_pages += count_pdf_pages(downloaded_path)
                        os.remove(downloaded_path)  # Clean up downloaded file
                except Exception as e:
                    logging.error(f"Error processing {item} for file: {file_path}: {e}")
            logging.error(f"Last published date in {file_path}: {date}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
    return total_pages, os.path.splitext(os.path.basename(file_path))[0]

def update_results_json(results_file, equity, count):
    if os.path.exists(results_file):
        with open(results_file, 'r') as file:
            results = json.load(file)
    else:
        results = []

    results.append({'equity': equity, 'count': count})

    with open(results_file, 'w') as file:
        json.dump(results, file, indent=4)

def worker(file_path, results_file):
    total_pages, equity = process_json_file(file_path)
    update_results_json(results_file, equity, total_pages)

def load_existing_equities(results_file):
    """Load existing equities from the results file."""
    if not os.path.exists(results_file):
        return set()

    with open(results_file, 'r') as file:
        data = json.load(file)
        return set(item['equity'] for item in data)

def main(folder_path, results_file):
    file_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.json')]

    # Load existing equities
    existing_equities = load_existing_equities(results_file)

    with Pool(cpu_count()) as pool:
        for file_path in file_paths:
            equity_name = os.path.splitext(os.path.basename(file_path))[0]
            if equity_name in existing_equities:
                print(f"Skipping {file_path} as it is already in the results file.")
                continue
            pool.apply_async(worker, (file_path, results_file))

        pool.close()
        pool.join()

# Example usage
folder_path = 'Completed/US_Consumer_Discretionary'
results_file = 'Completed/us_Consumer_Discretionary.json'
main(folder_path, results_file)
