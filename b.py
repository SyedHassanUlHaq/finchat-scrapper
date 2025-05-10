import os
import json

def replace_quarter_with_int(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Loop through each object in the JSON data
    for obj in data:
        fiscal_quarter = obj.get('fiscal_quarter')

        # Check if fiscal_quarter is a string like 'Q1', 'Q2', etc.
        if isinstance(fiscal_quarter, str) and fiscal_quarter.startswith('Q'):
            # Extract the number from the string
            quarter_number = int(fiscal_quarter[1:])

            # Replace the string with the corresponding integer
            obj['fiscal_quarter'] = quarter_number

    # Save the modified data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

def process_json_files_in_folder(folder_path):
    # Loop over all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Call the function to process the JSON file
            replace_quarter_with_int(file_path)

# Example usage:
process_json_files_in_folder('Completed/US_consumer_staples')
