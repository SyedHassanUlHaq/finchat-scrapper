import os
import json
import csv
from collections import defaultdict

def generate_summary(directory, output_csv):
    summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    # Traverse the directory and subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    for entry in data:
                        if entry.get("periodicity") == "periodic":
                            equity_ticker = entry["equity_ticker"]
                            content_type = entry["content_type"]
                            fiscal_year = entry.get("fiscal_year")
                            if fiscal_year:
                                summary[equity_ticker][content_type][fiscal_year] += 1

    # Write the summary to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        header = ["equity_ticker", "content_type"] + sorted(
            {year for equity in summary.values() for content in equity.values() for year in content}
        )
        writer.writerow(header)

        # Write rows
        for equity_ticker, content_types in summary.items():
            for content_type, years in content_types.items():
                row = [equity_ticker, content_type]
                for year in header[2:]:
                    row.append(years.get(year, 0))
                writer.writerow(row)

if __name__ == "__main__":
    directory = "Completed/US_consumer_staples"
    output_csv = "summary.csv"
    generate_summary(directory, output_csv)
    print(f"Summary CSV generated")
