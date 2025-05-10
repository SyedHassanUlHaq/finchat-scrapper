import json

def process_json_file(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize variables
    total_count = 0
    object_count = len(data)

    # Sum the 'count' values
    for item in data:
        total_count += item['count']

    return total_count, object_count

# Example usage
file_path = 'JSONS/combined_count.json'  # Replace with the path to your JSON file
total_count, object_count = process_json_file(file_path)

print(f"Total count of all objects: {total_count}")
print(f"Number of objects: {object_count}")
