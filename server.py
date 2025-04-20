from main import scrape_event_names
import asyncio
lis = [("HSY", "sdahgsajdgsaj", "false"),
       (),
       (),
       (),]


for i in lis:
    asyncio.run(scrape_event_names(i[0], i[1], i[2]))
