import os
import json

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
            results[filename] = process_json_file(file_path)

    return results

# Specify the directory path
directory_path = 'Completed/US_consumer_staples'

# Process all JSON files in the directory
results = process_directory(directory_path)

# Print the results
for filename, missing_info in results.items():
    print(f"File: {filename}")
    for fiscal_year, missing_quarters in missing_info.items():
        print(f"Fiscal Year: {fiscal_year}, Missing Quarters: {missing_quarters}")
    print()
