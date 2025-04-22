import os

# List of prefixes
prefixes = [
    "PG", "KO", "PM", "PEP", "MO", "MDLZ", "CVS", "MCK", "CL", "COR",
    "KMB", "KR", "KVUE", "KDP", "MNST", "CTVA", "SYY", "GIS", "STZ",
    "CHD", "KHC", "HSY", "K", "ADM", "MKC", "CLX", "TSN", "CASY",
    "USFD", "CAG", "SJM", "PFGC", "TAP", "BG", "BRBR", "ACI", "HRL",
    "INGR", "COKE", "WBA", "LW", "CPB", "CELH", "POST", "BFB", "DAR",
    "SAM", "BFA", "IFF", "AVGO", "NVDA", "TXN", "QCOM", "AMD", "KLAC",
    "AMAT", "LRCX", "INTC", "ASML", "MPWR", "ADI", "NXPI", "MU", "TSM",
    "MCHP", "MRVL", "ON", "TER", "ENTG", "SWKS", "ONTO", "LSCC", "QRVO",
    "OLED", "MKSI", "ARM"
]

# Source folder
source_folder = 'Completed/US_consumer_staples/'

# Set to keep track of found prefixes
found_prefixes = set()

# Iterate over files in the source folder
for filename in os.listdir(source_folder):
    # Check if the file name starts with any of the prefixes
    for prefix in prefixes:
        if filename.startswith(prefix):
            found_prefixes.add(prefix)
            break

# Determine which prefixes were not found
not_found_prefixes = set(prefixes) - found_prefixes

# Print the prefixes that were not found
print("Prefixes not found:")
for prefix in not_found_prefixes:
    print(prefix)

print("Checking process completed.")
