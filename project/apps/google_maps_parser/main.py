import asyncio

from engine import GoogleMapsEngine


async def main():
    q = input('Enter your search query: ').strip() or 'Barbershop'
    addr = input('Enter the location you would like to search in: ').strip() \
        or 'Paris'
    zoom = float(input('[Optional] Enter google maps zoom: ').strip() or 12)

    engine = GoogleMapsEngine(q, addr, zoom)
    await engine.run()
    await engine.save_to_csv()
    print(engine.entries)

if __name__ == '__main__':
    asyncio.run(main())
