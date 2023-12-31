import asyncio
from playwright.async_api import async_playwright, Playwright, Browser, Page, ElementHandle
from time import sleep, time


query = 'спортазл'
browser_params = {'headless': False, 'proxy': None, 'slow_mo': 150}
page_params = {'java_script_enabled': True,
               'bypass_csp': True, 'locale': 'en-GB'}
# so that location is defined by the user, or get coords by input query city
coords = (51.0968431, 71.428286)
coords = list(map(str, coords))
url = f'https://www.google.com/maps/@{''.join(coords)},13z?entry=ttu'


async def run(playwright: Playwright):
    chromium = playwright.chromium

    browser: Browser = await chromium.launch(**browser_params)
    page: Page = await browser.new_page(**page_params)

    await page.goto('https://www.google.com/maps')
    await asyncio.sleep(3)

    # find by query
    # go over every search result
    # parse its telephone number and other information
    # once there are no more results, save data and exit

    await page.click('#searchboxinput')
    await page.keyboard.type(query, delay=20)
    await page.keyboard.press('Enter')
    await page.wait_for_selector('.hfpxzc')  # wait for results to appear

    end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')

    leftbar = await page.query_selector('[role="main"]')
    await leftbar.hover()
    sleep(5)
    print('Hovered on leftbar, ready to scroll')

    start_scroll_time = time()
    scroll_time_duration_s = 50

    while True:
        await page.mouse.wheel(0, 1000)
        sleep(0.2)
        print('Scroll down')

        end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')
        print('End locator:', end_locator)
        
        finish_scroll_time = time()
    
        if end_locator is not None:
            print('End locator found, breaking')
            break
        
        if finish_scroll_time - start_scroll_time > scroll_time_duration_s:
            print(f'Timeout exceed {scroll_time_duration_s} seconds. Breaking automatically')
            break
        
    link_elements = await page.query_selector_all('a.hfpxzc')
    print('Link elements:', link_elements)

    for link_element in link_elements:
        link = await link_element.get_attribute('href')
        print(link)

    print('Finished')
    sleep(999999)
    await browser.close()

# enter query
# scroll all the way down
# extract all hrefs of results
# go over each href and extract information
# save and format the info


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
