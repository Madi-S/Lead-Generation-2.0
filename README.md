# Lead-Generation 0.2.2

The updated version of my outdated dirty clumsy and having shockingly high amount of stars repository on Python - https://github.com/Madi-S/Lead-Generation

# Quickstart

```
import asyncio
from py_lead_generation import YelpEngine, GoogleMapsEngine

async def main() -> None:
    engine = GoogleMapsEngine('Barbershop', 'Paris')
    await engine.run()
    engine.save_to_csv()

    engine = YelpEngine('Pizza', 'Mexico, Pampanga, Philippines')
    await engine.run()
    engine.save_to_csv()

if __name__ == '__main__':
    asyncio.run(main())
```

# Current functionality
    - Parse Google Maps
    - Parse Yelp
    - Export collected data to a CSV file

# Expectations of this project:

    - Parse Google Maps and Yelp for telephone number, email, address and other information by given keyword
    - Somehow parse search results in Google Search for the same information using regex or other algorithm
    - Export all parsed data to csv or excel
    - For parsed emails send a message, which will be prevented from going to spam
    - For parsed telephone numbers send an SMS, which will b prevented from going to spam as well
