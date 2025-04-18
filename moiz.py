from main import scrape_events_names
import asyncio
lis = [
{"KHC", "https://finchat.io/company/NasdaqGS-KHC/investor-relations/", "false"},
{"HSY", "https://finchat.io/company/NYSE-HSY/investor-relations/", "false"},
{"K", "https://finchat.io/company/NYSE-K/investor-relations/", "false"},
{"ADM", "https://finchat.io/company/NYSE-ADM/investor-relations/", "false"},
{"MKC", "https://finchat.io/company/NYSE-MKC/investor-relations/", "false"},
{"CLX", "https://finchat.io/company/NYSE-CLX/investor-relations/", "false"},
{"TSN", "https://finchat.io/company/NYSE-TSN/investor-relations/", "false"},
{"CASY", "https://finchat.io/company/NasdaqGS-CASY/investor-relations/", "false"},
{"USFD", "https://finchat.io/company/NYSE-USFD/investor-relations/", "false"},
{"CAG", "https://finchat.io/company/NYSE-CAG/investor-relations/", "false"},
{"SJM", "https://finchat.io/company/NYSE-SJM/investor-relations/", "false"},
{"PFGC", "https://finchat.io/company/NYSE-PFGC/investor-relations/", "false"},
{"TAP", "https://finchat.io/company/NYSE-TAP/investor-relations/", "false"},
{"BG", "https://finchat.io/company/NYSE-BG/investor-relations/", "false"},
{"BRBR", "https://finchat.io/company/NYSE-BRBR/investor-relations/", "false"},
{"ACI", "https://finchat.io/company/NYSE-ACI/investor-relations/", "false"},
{"HRL", "https://finchat.io/company/NYSE-HRL/investor-relations/", "false"},
{"INGR", "https://finchat.io/company/NYSE-INGR/investor-relations/", "false"},
{"COKE", "https://finchat.io/company/NasdaqGS-COKE/investor-relations/", "false"},
{"WBA", "https://finchat.io/company/NasdaqGS-WBA/investor-relations/", "false"}

       ]

for i in lis:
    asyncio.run(scrape_events_names(i[0], i[1], i[2]))