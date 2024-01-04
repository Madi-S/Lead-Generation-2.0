# import asyncio

# from apps.google_maps.engine import GoogleMapsEngine


# async def main():
#     q = input('Enter your search query: ').strip() or 'Barbershop'
#     addr = input('Enter the location you would like to search in: ').strip() \
#         or 'Paris'
#     zoom = float(input('[Optional] Enter google maps zoom: ').strip() or 12)

#     engine = GoogleMapsEngine(q, addr, zoom)
#     await engine.run()
#     engine.save_to_csv()

# if __name__ == '__main__':
#     asyncio.run(main())

# TODO: MOVE SAME LOGIC, FUNCTIONS, CODE FROM YelpEngine and GoogleMapsEngine to BaseEngine and create tiny methods for two above methods so that they can function correctly

import asyncio
from apps.yelp.engine import YelpEngine


async def main():
    engine = YelpEngine('Pizza', 'Mexico, Pampanga, Philippines')
    await engine.run()
    engine.save_to_csv()


if __name__ == '__main__':
    asyncio.run(main())
