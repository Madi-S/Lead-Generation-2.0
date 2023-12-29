import asyncio
from playwright.async_api import async_playwright, Playwright, Browser, Page
from time import sleep


query = 'ресторан'
browser_params = {'headless': False, 'proxy': None, 'slow_mo': 150}
page_params = {'java_script_enabled':True, 'bypass_csp': True, 'locale':'en-GB'}
coords = (51.0968431,71.428286) # so that location is defined by the user, or get coords by input query city
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
    await page.wait_for_selector('.hfpxzc') # wait for results to appear
    
    end_text = 'You\'ve reached the end of the list.'
    end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')
    while not end_locator:
        # try to scroll down
        ...
        end_locator = await page.query_selector('.m6QErb.tLjsW.eKbjU')
    
    result_links = ...
    
    # i = 0
    # scroll_i = 0
    # while True:
    #     results = await page.query_selector_all('.hfpxzc')
    #     print(results)
    #     result = results[i]
    #     await result.click()
    #     print('visible', await result.is_visible())
    #     print('element', result.as_element())
    #     print('props', await result.get_properties())
    #     break
    
    
    sleep(999999)
    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())