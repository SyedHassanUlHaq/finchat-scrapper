import os

# List of prefixes
prefixes = [
    "MSFT", "AAPL", "NVDA", "META", "AVGO", "GOOGL", "CRM", "IBM",
    "ORCL", "GOOG", "PLTR", "NOW", "INTU", "ADBE", "QCOM", "TXN",
    "AMD", "AMAT", "PANW", "ADI", "KLAC", "INTC", "LRCX", "CRWD",
    "MU", "APH", "CDNS", "APP", "SNPS", "DASH", "FTNT", "ROP",
    "MSTR", "ADSK", "WDAY", "MRVL", "SNOW", "CTSH", "GLW", "TEAM",
    "NET", "IT", "DDOG", "ANSS", "HUBS", "GDDY", "TYL", "MPWR",
    "HPQ", "DELL", "CDW", "VRSN", "MCHP", "ZM", "ZS", "HPE", "PTC",
    "SMCI", "NTAP", "OKTA", "PINS", "NTNX", "GWRE", "DOCU", "FFIV",
    "TOST", "ON", "JBL", "GEN", "TWLO", "DT", "PSTG", "WDC", "TER",
    "MDB", "AKAM", "PAYC", "ENTG", "DOX", "MANH", "SWKS", "EPAM",
    "XTSLA", "DAY", "SNX", "MTCH", "COHR", "ESTC", "KD", "ALAB",
    "DBX", "MTSI", "BSY", "LSCC", "ONTO", "GTLB", "U", "OLED",
    "CFLT", "ARW", "QRVO", "APPF", "S", "PATH", "GLOB", "DLB",
    "SNDK", "AVT", "PEGA", "DXC", "IAC", "ALGM", "ZI"
]

# Source folder
source_folder = 'Completed/US_Technology/'

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
