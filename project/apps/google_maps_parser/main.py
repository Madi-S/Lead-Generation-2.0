import time
import asyncio
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Playwright, Browser, Page, BrowserType

from writer import CsvWriter


# query = input()
query = 'ресторан'
browser_params = {'headless': False, 'proxy': None, 'slow_mo': 150}
page_params = {'java_script_enabled': True,
               'bypass_csp': True, 'locale': 'en-GB'}
# so that location is defined by the user, or get coords by input query city
geolocator = Nominatim(user_agent='my-app')
# city = input()
# city = 'Astana'
# location = geolocator.geocode('Astana')
# coords = (location.latitude, location.longitude)
# print(coords)
coords = (51.0968431, 71.428286)
coords = list(map(str, coords))
url = f'https://www.google.com/maps/@{''.join(coords)},13z?entry=ttu'


async def run(playwright: Playwright) -> None:
    chromium: BrowserType = playwright.chromium

    browser: Browser = await chromium.launch(**browser_params)
    page: Page = await browser.new_page(**page_params)

    await page.goto('https://www.google.com/maps')
    await asyncio.sleep(3)

    await page.click('#searchboxinput')
    await page.keyboard.type(query, delay=20)
    await page.keyboard.press('Enter')
    await page.wait_for_selector('.hfpxzc')  # wait for results to appear

    end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')

    leftbar = await page.query_selector('[role="main"]')
    await leftbar.hover()
    await asyncio.sleep(0.5)
    print('Hovered on leftbar, ready to scroll')

    start_scroll_time = time.time()
    scroll_time_duration_s = 10  # 100

    while True:
        print('Scroll down')
        await page.mouse.wheel(0, 1000)
        await asyncio.sleep(4)

        end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')
        print('End locator:', end_locator)

        finish_scroll_time = time.time()

        if end_locator is not None:
            end_locator_text = await end_locator.text_content()
            print('End locator found, breaking', end_locator_text)
            break

        if finish_scroll_time - start_scroll_time > scroll_time_duration_s:
            print(f'Timeout exceed {
                  scroll_time_duration_s} seconds. Breaking automatically')
            break

    link_elements = await page.query_selector_all('a.hfpxzc')
    print('Link elements:', link_elements)

    links = []
    for link_element in link_elements:
        link = await link_element.get_attribute('href')
        links.append(link)

    info = []
    for link in links:
        print('Parsing', link)
        await page.goto(link)
        await asyncio.sleep(3)

        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.select_one('.DUwDvf.lfPIob').get_text()

        addr_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png'
        addr_img = soup.select_one(f'img[src="{addr_img_src}"]')
        addr = addr_img.parent.parent.parent.select_one('.Io6YTe').get_text() \
            if addr_img else '-'

        phone_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png'
        phone_img = soup.select_one(f'img[src="{phone_img_src}"]')
        phone = phone_img.parent.parent.parent.select_one('.Io6YTe').get_text() \
            if phone_img else '-'

        website_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png'
        website_img = soup.select_one(f'img[src="{website_img_src}"]')
        website = website_img.parent.parent.parent.select_one('.Io6YTe').get_text() \
            if website_img else ''

        print('Title', title)
        print('Address', addr)
        print('Phone', phone)
        print('Website', website)
        info.append({
            'Title': title,
            'Address': addr,
            'PhoneNumber': phone,
            'WebsiteURL': website
        })

    print('Finished parsing')
    # await asyncio.sleep(999999)
    await browser.close()

    print('Writing info to csv')
    filename = 'google_maps_leads.csv'
    fn = ['Title', 'Address', 'PhoneNumber', 'WebsiteURL']
    csv_writer = CsvWriter(filename, fn)
    csv_writer.append(info)



async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
