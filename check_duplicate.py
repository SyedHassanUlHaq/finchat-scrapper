import json

def process_json_file(file_path):
    # Read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize variables
    equity_counts = {}
    duplicates = []

    # Count occurrences of each equity
    for item in data:
        equity = item['equity']
        if equity in equity_counts:
            equity_counts[equity] += 1
        else:
            equity_counts[equity] = 1

    # Identify duplicates
    for equity, count in equity_counts.items():
        if count > 1:
            duplicates.append(equity)

    return duplicates

# Example usage
file_path = 'JSONS/us_tech.json'  # Replace with the path to your JSON file
duplicates = process_json_file(file_path)

if duplicates:
    print("Duplicate equities found:")
    for equity in duplicates:
        print(equity)
else:
    print("No duplicate equities found.")
