import os
import shutil

# List of prefixes
prefixes = [
    "AVGO", "NVDA", "TXN", "QCOM", "AMD", "KLAC", "AMAT", "LRCX",
    "INTC", "ASML", "MPWR", "ADI", "NXPI", "MU", "TSM", "MCHP",
    "MRVL", "ON", "TER", "ENTG", "SWKS", "ONTO", "LSCC", "QRVO",
    "OLED", "MKSI", "ARM"
]

# Source and destination folders
source_folder = 'Completed/'
destination_folder = 'Completed/US_consumer_staples/'

# Ensure the destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# Iterate over files in the source folder
for filename in os.listdir(source_folder):
    # Check if the file name starts with any of the prefixes
    if any(filename.startswith(prefix) for prefix in prefixes):
        # Full file path
        source_file = os.path.join(source_folder, filename)
        destination_file = os.path.join(destination_folder, filename)

        # Move the file
        shutil.move(source_file, destination_file)
        print(f'Moved: {filename}')

print("File moving process completed.")
