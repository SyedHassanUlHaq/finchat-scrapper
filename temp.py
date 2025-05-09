import os
import json
import requests
import time
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from utils.upload_to_r2 import upload_to_r2  # Import the upload_to_r2 function

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    fiscal_year_quarters = {}

    for item in data:
        if item["content_type"] == "earnings_transcript" and item["fiscal_year"] is not None:
            fiscal_year = item["fiscal_year"]
            fiscal_quarter = item["fiscal_quarter"]

            if fiscal_year not in fiscal_year_quarters:
                fiscal_year_quarters[fiscal_year] = set()

            fiscal_year_quarters[fiscal_year].add(fiscal_quarter)

    missing_transcripts = {}

    for fiscal_year, quarters in fiscal_year_quarters.items():
        missing_quarters = [q for q in range(1, 5) if q not in quarters]
        if missing_quarters:
            missing_transcripts[fiscal_year] = missing_quarters

    return missing_transcripts

def process_directory(directory_path):
    results = {}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            results[filename] = {
                "missing_info": process_json_file(file_path),
                "file_path": file_path
            }

    return results

def create_pdf_for_missing_transcripts(directory_path, results):
    for filename, result in results.items():
        file_path = result["file_path"]
        missing_info = result["missing_info"]

        # Extract equity ticker from the filename
        equity_ticker = filename.split('_')[0]

        for fiscal_year, missing_quarters in missing_info.items():
            for quarter in missing_quarters:
                # API endpoint and parameters
                url = "https://financialmodelingprep.com/stable/earning-call-transcript"
                params = {
                    "symbol": equity_ticker,
                    "year": fiscal_year,
                    "quarter": quarter,
                    "apikey": "P3jycMiIDB3fujYc6f2YpwfOBIzUSag1"
                }

                # Fetch the data from the API
                response = requests.get(url, params=params)

                # Check if the request was successful
                if response.status_code != 200:
                    print(f"Failed to fetch data for {equity_ticker} {fiscal_year} Q{quarter}. Status code: {response.status_code}")
                    continue

                try:
                    data = response.json()
                except json.JSONDecodeError:
                    print(f"Failed to decode JSON from response for {equity_ticker} {fiscal_year} Q{quarter}. Response content: {response.content}")
                    continue

                if data:
                    transcript_content = data[0]["content"]
                    date = data[0]["date"]  # Extract the date from the API response

                    # Create a PDF file
                    pdf_filename = f"transcript_{equity_ticker}_{fiscal_year}_Q{quarter}.pdf"
                    doc = SimpleDocTemplate(pdf_filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
                    styles = getSampleStyleSheet()

                    # Create a list to hold the flowables
                    flowables = []

                    # Add the transcript content as a Paragraph
                    paragraph = Paragraph(transcript_content, styles["Normal"])
                    flowables.append(paragraph)

                    # Add a spacer to ensure the text doesn't overflow
                    flowables.append(Spacer(1, 0.2 * inch))

                    # Build the PDF document
                    doc.build(flowables)

                    # Upload the PDF to R2
                    r2_folder = f"{equity_ticker}/{date}/{pdf_filename}/"
                    r2_url = upload_to_r2(pdf_filename, r2_folder, test_run='false')

                    # Create the JSON object
                    json_object = {
                        "equity_ticker": equity_ticker,
                        "geography": "US",
                        "content_name": f"{equity_ticker} Q{quarter} {fiscal_year} Transcript",
                        "file_type": "pdf",
                        "content_type": "earnings_transcript",
                        "published_date": date,
                        "fiscal_date": date,
                        "fiscal_year": fiscal_year,
                        "fiscal_quarter": quarter,
                        "r2_url": r2_url,
                        "periodicity": "periodic"
                    }

                    # Append the JSON object to the respective file
                    with open(file_path, 'r+') as file:
                        file_data = json.load(file)
                        file_data.append(json_object)
                        file.seek(0)
                        json.dump(file_data, file, indent=4)
                        file.truncate()

                    print(f"Transcript content for {equity_ticker} {fiscal_year} Q{quarter} has been saved to {pdf_filename} and uploaded to R2: {r2_url}")

# Specify the directory path
directory_path = 'Completed/US_consumer_staples'

# Process all JSON files in the directory
results = process_directory(directory_path)

# Create PDFs for missing transcripts
create_pdf_for_missing_transcripts(directory_path, results)
