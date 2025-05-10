import os
import json

def replace_null_strings_with_none(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Loop through each object in the JSON data
    for obj in data:
        # Check if fiscal_year is the string 'null' and replace with None
        if obj.get('fiscal_year') == 'null':
            obj['fiscal_year'] = None

        # Check if fiscal_quarter is the string 'null' and replace with None
        if obj.get('fiscal_quarter') == 'null':
            obj['fiscal_quarter'] = None

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
            replace_null_strings_with_none(file_path)

# Example usage:
process_json_files_in_folder('Completed/US_consumer_staples')
