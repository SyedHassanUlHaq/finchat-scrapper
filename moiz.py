from main import scrape_events_names
import asyncio
lis = [
    
    #77-105
       # {"KHC", "https://finchat.io/company/NasdaqGS-KHC/investor-relations/", "false"},
       # {"HSY", "https://finchat.io/company/NYSE-HSY/investor-relations/", "false"},
       # {"K", "https://finchat.io/company/NYSE-K/investor-relations/", "false"},
       # {"ADM", "https://finchat.io/company/NYSE-ADM/investor-relations/", "false"},
       # {"MKC", "https://finchat.io/company/NYSE-MKC/investor-relations/", "false"},
       # {"CLX", "https://finchat.io/company/NYSE-CLX/investor-relations/", "false"},
       # {"TSN", "https://finchat.io/company/NYSE-TSN/investor-relations/", "false"},
       # {"CASY", "https://finchat.io/company/NasdaqGS-CASY/investor-relations/", "false"},
       # {"USFD", "https://finchat.io/company/NYSE-USFD/investor-relations/", "false"},
       # {"CAG", "https://finchat.io/company/NYSE-CAG/investor-relations/", "false"},
       # {"SJM", "https://finchat.io/company/NYSE-SJM/investor-relations/", "false"},
       # {"PFGC", "https://finchat.io/company/NYSE-PFGC/investor-relations/", "false"},
       # {"TAP", "https://finchat.io/company/NYSE-TAP/investor-relations/", "false"},
       # {"BG", "https://finchat.io/company/NYSE-BG/investor-relations/", "false"},
       # {"BRBR", "https://finchat.io/company/NYSE-BRBR/investor-relations/", "false"},
       # {"ACI", "https://finchat.io/company/NYSE-ACI/investor-relations/", "false"},
       # {"HRL", "https://finchat.io/company/NYSE-HRL/investor-relations/", "false"},
       # {"INGR", "https://finchat.io/company/NYSE-INGR/investor-relations/", "false"},
       # {"COKE", "https://finchat.io/company/NasdaqGS-COKE/investor-relations/", "false"},
       # {"WBA", "https://finchat.io/company/NasdaqGS-WBA/investor-relations/", "false"}
       # {"LW", "https://finchat.io/company/NYSE-LW/investor-relations/", "false"},
       # {"CPB", "https://finchat.io/company/NasdaqGS-CPB/investor-relations/", "false"},
       # {"CELH", "https://finchat.io/company/NasdaqCM-CELH/investor-relations/", "false"},
       # {"POST", "https://finchat.io/company/NYSE-POST/investor-relations/", "false"},
       # {"BFB", "https://finchat.io/company/NYSE-BF.B/investor-relations/", "false"},
       # {"DAR", "https://finchat.io/company/NYSE-DAR/investor-relations/", "false"},
       # {"SAM", "https://finchat.io/company/NYSE-SAM/investor-relations/", "false"},
       # {"BFA", "https://finchat.io/company/NYSE-BF.B/investor-relations/", "false"},
       # {"IFF", "https://finchat.io/company/NYSE-IFF/investor-relations/", "false"}


       #23-42
       {"F", "https://finchat.io/company/NYSE-F/investor-relations/", "false"},
       {"DHI", "https://finchat.io/company/NYSE-DHI/investor-relations/", "false"},
       {"EBAY", "https://finchat.io/company/NasdaqGS-EBAY/investor-relations/", "false"},
       {"LULU", "https://finchat.io/company/NasdaqGS-LULU/investor-relations/", "false"},
       {"GRMN", "https://finchat.io/company/NYSE-GRMN/investor-relations/", "false"},
       {"TSCO", "https://finchat.io/company/NasdaqGS-TSCO/investor-relations/", "false"},
       {"LEN", "https://finchat.io/company/NYSE-LEN/investor-relations/", "false"},
       {"DRI", "https://finchat.io/company/NYSE-DRI/investor-relations/", "false"},
       {"NVR", "https://finchat.io/company/NYSE-NVR/investor-relations/", "false"},
       {"PHM", "https://finchat.io/company/NYSE-PHM/investor-relations/", "false"},
       {"CCL", "https://finchat.io/company/NYSE-CCL/investor-relations/", "false"},
       {"WSM", "https://finchat.io/company/NYSE-WSM/investor-relations/", "false"},
       {"EXPE", "https://finchat.io/company/NasdaqGS-EXPE/investor-relations/", "false"},
       {"DECK", "https://finchat.io/company/NYSE-DECK/investor-relations/", "false"},
       {"ULTA", "https://finchat.io/company/NasdaqGS-ULTA/investor-relations/", "false"},
       {"DPZ", "https://finchat.io/company/NasdaqGS-DPZ/investor-relations/", "false"},
       {"GPC", "https://finchat.io/company/NYSE-GPC/investor-relations/", "false"},
       {"TPR", "https://finchat.io/company/NYSE-TPR/investor-relations/", "false"},
       {"APTV", "https://finchat.io/company/NYSE-APTV/investor-relations/", "false"},
       {"KMX", "https://finchat.io/company/NYSE-KMX/investor-relations/", "false"},
       ]

for i in lis:
    asyncio.run(scrape_events_names(i[0], i[1], i[2]))
                