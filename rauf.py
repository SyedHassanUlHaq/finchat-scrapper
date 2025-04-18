from main import scrape_event_names
import asyncio
lis = [("PG", "https://finchat.io/company/NYSE-PG/investor-relations/", 'true'),
 ("KO", "https://finchat.io/company/NYSE-KO/investor-relations/", "false"),
 ("PM", "https://finchat.io/company/NYSE-PM/investor-relations/", 'false'),
 ("PEP", "https://finchat.io/company/NasdaqGS-PEP/investor-relations/", 'false'),
 ("MO", "https://finchat.io/company/NYSE-MO/investor-relations/", 'false'),
 ("MDLZ", "https://finchat.io/company/NasdaqGS-MDLZ/investor-relations/", "false"),
 ("CVS", 'https://finchat.io/company/NYSE-CVS/investor-relations/', 'false'),
 ("MCK", "https://finchat.io/company/NYSE-MCK/investor-relations/", 'false'),
 ("CL", "https://finchat.io/company/NYSE-CL/investor-relations/", 'false'),
 ("COR", "https://finchat.io/company/NYSE-COR/investor-relations/", "false"),
 ("KMB", "https://finchat.io/company/NYSE-KMB/investor-relations/", "false"),
 ]

for i in lis:
    asyncio.run(scrape_event_names(i[0], i[1], i[2]))