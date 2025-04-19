from main import scrape_event_names
import asyncio

lis = [("TSLA", "https://finchat.io/company/NasdaqGS-TSLA/investor-relations/", 'false'),
 ("AMZN", "https://finchat.io/company/NasdaqGS-AMZN/investor-relations/", "false"),
 ("HD", "https://finchat.io/company/NYSE-HD/investor-relations/", 'false'),
 ("MCD", "https://finchat.io/company/NYSE-MCD/investor-relations/", 'false'),
 ("BKNG", "https://finchat.io/company/NasdaqGS-BKNG/investor-relations/", 'false'),
 ("TJX", "https://finchat.io/company/NYSE-TJX/investor-relations/", "false"),
 ("LOW", 'https://finchat.io/company/NYSE-TJX/investor-relations/', 'false'),
 ("SBUX", "https://finchat.io/company/NasdaqGS-SBUX/investor-relations/", 'false'),
 ("ORLY", "https://finchat.io/company/NasdaqGS-ORLY/investor-relations/", 'false'),
 ("NKE", "https://finchat.io/company/NYSE-NKE/investor-relations/", "false"),
 ("CMG", "https://finchat.io/company/NYSE-CMG/investor-relations/", "false"),
 ("AZO", "https://finchat.io/company/NYSE-AZO/investor-relations/", "false"),
 ("DASH", "https://finchat.io/company/NasdaqGS-DASH/investor-relations/", "false"),
 ("HLT", "https://finchat.io/company/NYSE-HLT/investor-relations/", "false"),
 ("MAR", "https://finchat.io/company/NasdaqGS-MAR/investor-relations/", "false"),
 ("ABNB", "https://finchat.io/company/NasdaqGS-ABNB/investor-relations/", "false"),
 ("RCL", "https://finchat.io/company/NYSE-RCL/investor-relations/", "false"),
 ("GM", "https://finchat.io/company/NYSE-GM/investor-relations/", "false"),
 ("ROST", "https://finchat.io/company/NasdaqGS-ROST/investor-relations/", "false"),
 ("YUM", "https://finchat.io/company/NYSE-YUM/investor-relations/", "false"),
 ]

for i in lis:
    asyncio.run(scrape_event_names(i[0], i[1], i[2]))