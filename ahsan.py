from main import scrape_event_names
import asyncio
# 3-22 % 43-47 
lis = [("ARW", "https://finchat.io/company/NYSE-ARW/investor-relations/", "false"),
 ("QRVO", "https://finchat.io/company/NasdaqGS-QRVO/investor-relations/", "false"),
 ]

for i in lis:
    asyncio.run(scrape_event_names(i[0], i[1], i[2]))