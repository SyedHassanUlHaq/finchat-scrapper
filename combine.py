import json
import argparse
import os

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def save_json(data, output_path):
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Combined JSON saved to: {output_path}")

def combine_json_files(file1, file2, output_file):
    data1 = load_json(file1)
    data2 = load_json(file2)

    if not isinstance(data1, list) or not isinstance(data2, list):
        raise ValueError("Both JSON files must contain a list of objects.")

    combined = data1 + data2
    save_json(combined, output_file)

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Combine two JSON files.")
    # parser.add_argument("file1", help="Path to the first JSON file")
    # parser.add_argument("file2", help="Path to the second JSON file")
    # parser.add_argument("-o", "--output", default="combined.json", help="Output file name (default: combined.json)")
    # args = parser.parse_args()

    # combine_json_files(args.file1, args.file2, args.output)
    json_dir = "JSONS"
    for file_name in os.listdir(json_dir):
        if file_name.endswith("_investor_relations.json"):
            ticker = file_name.split("_")[0]
            file1 = os.path.join(json_dir, f"{ticker}_investor_relations.json")
            file2 = os.path.join(json_dir, f"{ticker}_sec_filings.json")
            output_file = os.path.join(json_dir, f"{ticker}_investor_relations_sec.json")
            
            if os.path.exists(file1) and os.path.exists(file2):
                try:
                    combine_json_files(file1, file2, output_file)
                except Exception as e:
                    print(f"Error combining files for {ticker}: {e}")