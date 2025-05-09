import os
import json

def reorder_json_objects(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Separate objects with '10-K' or '10-Q' in content_name
    priority_objects = []
    other_objects = []

    for obj in data:
        content_name = obj.get('content_name', '')
        if '10-K' in content_name or '10-Q' in content_name:
            priority_objects.append(obj)
        else:
            other_objects.append(obj)

    # Combine the lists with priority objects first
    reordered_data = priority_objects + other_objects

    # Save the reordered data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(reordered_data, file, indent=4)

def process_json_files_in_folder(folder_path):
    # Loop over all the files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Call the function to process the JSON file
            reorder_json_objects(file_path)

# Example usage:
process_json_files_in_folder('Completed/US_consumer_staples')
