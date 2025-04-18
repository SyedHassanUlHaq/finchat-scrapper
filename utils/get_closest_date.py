import json
from datetime import datetime

def find_closest_date(json_path, target_date_str):
    """
    Finds the date in the JSON file that is closest to the target date.

    Parameters:
    - json_path (str): Path to the JSON file.
    - target_date_str (str): Target date in 'YYYY-MM-DD' format.

    Returns:
    - str: The closest date in 'YYYY-MM-DD' format, or None if not found.
    """
    # Convert the target date string to a datetime object
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Error: '{target_date_str}' is not in the correct format 'YYYY-MM-DD'.")
        return None

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file: {e}")
        return None

    # Initialize variables to track the closest date
    closest_date = None
    min_diff = None

    # Iterate through each item in the JSON data
    for item in data:
        date_str = item.get('published_date')
        if not date_str:
            continue  # Skip if 'published_date' is missing

        try:
            current_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue  # Skip if date format is incorrect

        # Calculate the absolute difference in days
        diff = abs((current_date - target_date).days)

        # Update the closest date if this is the smallest difference so far
        if (min_diff is None) or (diff < min_diff):
            min_diff = diff
            closest_date = current_date

    # Return the closest date as a string in 'YYYY-MM-DD' format
    return closest_date.strftime("%Y-%m-%d") if closest_date else None

