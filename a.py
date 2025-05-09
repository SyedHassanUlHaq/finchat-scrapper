import os
import json

def check_missing_earning_transcripts(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize a dictionary to keep track of earning_transcript counts per fiscal year and quarter
    earning_transcripts = {}

    # Loop through each object in the JSON data
    for obj in data:
        fiscal_year = obj['fiscal_year']
        fiscal_quarter = obj['fiscal_quarter']
        content_type = obj['content_type']

        # Check if the content_type is 'earning_transcript'
        if content_type == 'earning_transcript':
            if fiscal_year not in earning_transcripts:
                earning_transcripts[fiscal_year] = set()
            earning_transcripts[fiscal_year].add(fiscal_quarter)

    # Check for missing earning_transcript entries
    for fiscal_year in earning_transcripts:
        missing_quarters = [q for q in range(1, 5) if q not in earning_transcripts[fiscal_year]]
        for quarter in missing_quarters:
            print(f"Missing earning_transcript for fiscal year {fiscal_year}, quarter {quarter}")

def process_json_files_in_folder(folder_path):
    # Loop over all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            print(f"Processing file: {file_path}")

            # Call the function to process the JSON file
            check_missing_earning_transcripts(file_path)

# Example usage:
process_json_files_in_folder('Completed/US_consumer_staples')
