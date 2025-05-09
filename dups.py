import json

def check_and_remove_reports(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize dictionaries to keep track of report counts per year
    annual_report_counts = {}
    quarterly_report_counts = {}

    # Initialize a list to store objects that meet the criteria
    compliant_objects = []

    # Loop through each object in the JSON data
    for obj in data:
        fiscal_year = obj['fiscal_year']
        content_type = obj['content_type']
        content_name = obj['content_name']

        # Check if the content_type is 'annual_report'
        if content_type == 'annual_report':
            if fiscal_year in annual_report_counts:
                annual_report_counts[fiscal_year] += 1
            else:
                annual_report_counts[fiscal_year] = 1

            # Check if there are more than 1 'annual_report' for the given year
            if annual_report_counts[fiscal_year] <= 1 or '10-K' in content_name:
                compliant_objects.append(obj)

        # Check if the content_type is 'quarterly_report'
        elif content_type == 'quarterly_report':
            if fiscal_year in quarterly_report_counts:
                quarterly_report_counts[fiscal_year] += 1
            else:
                quarterly_report_counts[fiscal_year] = 1

            # Check if there are more than 3 'quarterly_report' for the given year
            if quarterly_report_counts[fiscal_year] <= 3 or '10-Q' in content_name:
                compliant_objects.append(obj)

        else:
            compliant_objects.append(obj)

    # Save the compliant objects back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(compliant_objects, file, indent=4)

# Example usage:
import os
import json

def check_and_remove_reports(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Initialize dictionaries to keep track of report counts per year
    annual_report_counts = {}
    quarterly_report_counts = {}

    # Initialize a list to store objects that meet the criteria
    compliant_objects = []

    # Loop through each object in the JSON data
    for obj in data:
        fiscal_year = obj['fiscal_year']
        content_type = obj['content_type']
        content_name = obj['content_name']

        # Check if the content_type is 'annual_report'
        if content_type == 'annual_report':
            if fiscal_year in annual_report_counts:
                annual_report_counts[fiscal_year] += 1
            else:
                annual_report_counts[fiscal_year] = 1

            # Check if there are more than 1 'annual_report' for the given year
            if annual_report_counts[fiscal_year] <= 1 or '10-K' in content_name:
                compliant_objects.append(obj)

        # Check if the content_type is 'quarterly_report'
        elif content_type == 'quarterly_report':
            if fiscal_year in quarterly_report_counts:
                quarterly_report_counts[fiscal_year] += 1
            else:
                quarterly_report_counts[fiscal_year] = 1

            # Check if there are more than 3 'quarterly_report' for the given year
            if quarterly_report_counts[fiscal_year] <= 3 or '10-Q' in content_name:
                compliant_objects.append(obj)

        else:
            compliant_objects.append(obj)

    # Save the compliant objects back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(compliant_objects, file, indent=4)

def process_json_files_in_folder(folder_path):
    # Loop over all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)
            print(f"Processing file: {file_path}")
            if 'ANSS' in file_path:
                continue

            # Call the function to process the JSON file
            check_and_remove_reports(file_path)

# Example usage:
process_json_files_in_folder('Completed/US_consumer_staples')
