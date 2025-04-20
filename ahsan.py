from main import scrape_event_names
import asyncio
# 3-22 % 43-47 
lis = [("AKAM", "https://finchat.io/company/NasdaqGS-AKAM/investor-relations/", 'false'),
 ("PAYC", "https://finchat.io/company/NYSE-PAYC/investor-relations/", "false"),
 ("ENTG", "https://finchat.io/company/NasdaqGS-ENTG/investor-relations/", 'false'),
 ("DOX", "https://finchat.io/company/NasdaqGS-DOX/investor-relations/", 'false'),
 ("MANH", "https://finchat.io/company/NasdaqGS-MANH/investor-relations/", 'false'),
 ("SWKS", "https://finchat.io/company/NasdaqGS-SWKS/investor-relations/", "false"),
 ("EPAM", 'https://finchat.io/company/NYSE-EPAM/investor-relations/', 'false'),
 ("DAY", "https://finchat.io/company/NYSE-DAY/investor-relations/", 'false'),
 ("SNX", "https://finchat.io/company/NYSE-SNX/investor-relations/", 'false'),
 ("MTCH", "https://finchat.io/company/NasdaqGS-MTCH/investor-relations/", "false"),
 ("COHR", "https://finchat.io/company/NYSE-COHR/investor-relations/", "false"),
 ("ESTC", "https://finchat.io/company/NYSE-ESTC/investor-relations/", "false"),
 ("KD", "https://finchat.io/company/NYSE-KD/investor-relations/", "false"),
 ("ALAB", "https://finchat.io/company/NasdaqGS-ALAB/investor-relations/", "false"),
 ("DBX", "https://finchat.io/company/NasdaqGS-DBX/investor-relations/", "false"),
 ("MTSI", "https://finchat.io/company/NasdaqGS-MTSI/investor-relations/", "false"),
 ("BSY", "https://finchat.io/company/NasdaqGS-BSY/investor-relations/", "false"),
 ("LSCC", "https://finchat.io/company/NasdaqGS-LSCC/investor-relations/", "false"),
 ("ONTO", "https://finchat.io/company/NYSE-ONTO/investor-relations/", "false"),
 ("GTLB", "https://finchat.io/company/NasdaqGS-GTLB/investor-relations/", "false"),
 ("U", "https://finchat.io/company/NYSE-U/investor-relations/", "false"),
 ("OLED", "https://finchat.io/company/NasdaqGS-OLED/investor-relations/", "false"),
 ("CFLT", "https://finchat.io/company/NasdaqGS-CFLT/investor-relations/", "false"),
 ("ARW", "https://finchat.io/company/NYSE-ARW/investor-relations/", "false"),
 ("QRVO", "https://finchat.io/company/NasdaqGS-QRVO/investor-relations/", "false"),
 ]

for i in lis:
    asyncio.run(scrape_event_names(i[0], i[1], i[2]))