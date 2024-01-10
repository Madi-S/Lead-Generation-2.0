import asyncio

from apps.yelp.engine import YelpEngine
from apps.google_maps.engine import GoogleMapsEngine


async def main() -> None:
    q = input('Enter your search query: ').strip() or 'Barbershop'
    addr = input('Enter the location you would like to search in: ').strip() \
        or 'Paris'
    zoom = float(input('[Optional] Enter google maps zoom: ').strip() or 12)

    engine = GoogleMapsEngine(q, addr, zoom)
    await engine.run()
    engine.save_to_csv()

    engine = YelpEngine('Pizza', 'Mexico, Pampanga, Philippines')
    await engine.run()
    engine.save_to_csv()

if __name__ == '__main__':
    asyncio.run(main())
