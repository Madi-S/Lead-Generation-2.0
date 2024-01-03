import time
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import Playwright, Browser, Page, BrowserType, ElementHandle, async_playwright

from utils import get_coords_by_location
from writer import CsvWriter


class GoogleMapsEngine:
    '''
    GoogleMapsEngine

    [CONSTANT] `BASE_URL` - base url for google maps website with substitute search query, coordinates and zoom 

    [EDITABLE] `BROWSER_PARAMS` - chromiun browser parameters configuration from playwright, additional parameters can be set if needed

    [EDITABLE] `PAGE_PARAMS` - browser page parameters configuration from playwright, additional parameters can be set if needed

    [EDITABLE] `SCROLL_TIME_DURATION_S` - scroll time duration to view the search results, preferably should be not less than 100, for testing purposes can be decreased

    [CONSTANT] `FIELD_NAMES` - field names of scraped data, extracts data entries to csv file based on these field names

    Usage:

    `engine = GoogleMapsEngine(*args, **kwargs)`

    `await engine.run()`

    `await engine.save_to_csv()`

    `print(engine.entries)`

    '''
    BASE_URL = 'https://www.google.com/maps/search/{query}/@{coords},{zoom}z/data=!3m1!4b1?entry=ttu'
    BROWSER_PARAMS = {'headless': False, 'proxy': None, 'slow_mo': 150}
    PAGE_PARAMS = {'java_script_enabled': True, 'bypass_csp': True}
    SCROLL_TIME_DURATION_S = 10
    SLEEP_PER_SCROLL_S = 4
    FIELD_NAMES = ['Title', 'Address', 'PhoneNumber', 'WebsiteURL']

    def __init__(self, query: str, location: str, zoom: int | float = 12) -> None:
        '''
        `query: str` - what are you looking for? e.g., `gym`
        `location: str` - where are you looking for that query? e.g., `Astana`
        `zoom: int | float` - google maps zoom e.g., `8.75`

        Creates `GoogleMapsEngine` instance
        '''
        self._entries = []
        self.zoom = zoom
        self.query = query
        self.location = location
        self.coords = get_coords_by_location(self.location)
        self.search_query = f'{self.query}%20{self.location}'
        self.url = self.BASE_URL.format(
            query=self.search_query, coords=','.join(self.coords), zoom=self.zoom
        )

    async def run(self) -> None:
        '''
        Uses headles webdriver powered by Playwright

        Creates a web url based on initialized parameters

        Parses results by given query and url one by one

        Assigns collected results to `.entries`

        To save the results call `.save_to_csv()` method after       
        '''
        async with async_playwright() as playwright:
            self.playwright: Playwright = playwright
            await self._setup_browser()
            await self._open_url_and_wait(self.url)
            urls: list[str] = await self._get_search_results_urls()
            self._entries: list[dict] = await self._get_search_results_entries(urls)
            await self.browser.close()

    async def save_to_csv(self, filename: str = 'google_maps_leads.csv') -> None:
        '''
        `filename: str='google_maps_leads.csv'` filename to save entries in, must be .csv filename

        If file with such name already exists, it will not overwrite it but append newly found entries to existing ones

        If file with such name does not exist, it will create a new csv file with predetermined fieldnames
        '''
        if not filename.endswith('.csv'):
            raise ValueError('Use .csv file extension')
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to save them'
            )
        csv_writer = CsvWriter(filename, self.FIELD_NAMES)
        csv_writer.append(self._entries)

    @property
    def entries(self) -> list[dict]:
        '''
        Returns `list[dict]` typed entries once `.run()` method was called
        '''
        if not self._entries:
            raise NotImplementedError(
                'Entries are empty, call .run() method first to create them'
            )
        return self._entries

    @entries.setter
    def entries(self, _) -> None:
        '''
        You cannot do that ;)

        Made for durability reasons
        '''
        raise ValueError('Cannot set value to data. This is not allowed')

    async def _setup_browser(self) -> None:
        '''
        Sets up the browser by initializing `playwright.chromiun` and `Browser` along with `Page` after
        '''
        chromium: BrowserType = self.playwright.chromium
        self.browser: Browser = await chromium.launch(**self.BROWSER_PARAMS)
        self.page: Page = await self.browser.new_page(**self.PAGE_PARAMS)

    async def _open_url_and_wait(self, url: str, sleep_duration_s: int = 3) -> None:
        '''
        `url: str` - url to open
        `sleep_duration_s: int = 3` - amount of seconds to wait for the page to load before any operations on that page

        Navigates to initialized `self.url` and waits for `sleep_duration_s` seconds
        '''
        await self.page.goto(url)
        await asyncio.sleep(sleep_duration_s)

    async def _get_search_results_urls(self) -> list[str]:
        '''
        Goes through the search results for `GoogleMapsEngine.SCROLL_TIME_DURATION_S` seconds

        Waits for `GoogleMapsEngine.SLEEP_PER_SCROLL_S` seconds so that GoogleMaps will not output endless load, aka simulate human-like activity

        Or scrapes the results urls, once the are no more results
        '''
        async def hover_search_results() -> None:
            '''
            Hovers on leftbar, where search results are located

            Needed so that scroll function is used properly - not on the map but on the search results div
            '''
            leftbar = await self.page.query_selector('[role="main"]')
            await leftbar.hover()
            await asyncio.sleep(0.5)

        async def scroll_and_sleep(delta_y: int = 1000) -> None:
            '''
            `delta_y: int = 1000` pixel units to scroll down along y-axis

            Scrolls down by `delta_y` and waits for `GoogleMapsEngine.SCROLL_TIME_DURATION_S` seconds
            '''
            await self.page.mouse.wheel(0, delta_y)
            await asyncio.sleep(self.SLEEP_PER_SCROLL_S)

        async def end_locator_is_present() -> bool:
            '''
            Retunrs `end_locator` as boolean value, which correlates with the possible end of the search results

            Once `end_locator` is Truthy, aka ElemenetHandle, it means that there is nothing more to scroll
            '''
            end_locator = await self.page.query_selector('.m6QErb.tLjsW.eKbjU')
            return bool(end_locator)

        async def scrape_urls() -> list[str]:
            '''
            Should be called once page is being scrolled all the way down (`end_locator` found) or `GoogleMapsEngine.SCROLL_TIME_DURATION_S` duration limit is exceeded

            Returns `list[str]` typed scraped urls list using query_selector
            '''
            urls = []
            link_elements = await self.page.query_selector_all('a.hfpxzc')
            for link_element in link_elements:
                url = await link_element.get_attribute('href')
                urls.append(url)
            return urls

        await hover_search_results()
        start_scroll_time = time.time()

        while True:
            await scroll_and_sleep()
            finish_scroll_time = time.time()
            if (await end_locator_is_present()) or (finish_scroll_time - start_scroll_time > self.SCROLL_TIME_DURATION_S):
                break

        urls = await scrape_urls()
        return urls

    async def _get_search_results_entries(self, urls: list[str]) -> list[dict]:
        '''
        `urls: list[str]` - list of urls for google maps entities to scrape for

        Goes over each url in the list and retreives data from opening page one by one

        Searches for data using exact image source values selectors, no other unique way to extract data using selectors is not found yet

        Returns `list[dict]` typed search result entries for each seperate given url from `urls`
        '''
        def parse_data_with_soup(html: str) -> list[str]:
            '''
            `html: str` - html representation of the page to parse

            Returns `list[dict]` typed parsed data - `[title, addr, phone, website]`
            '''
            soup = BeautifulSoup(html, 'html.parser')

            title = soup.select_one('.DUwDvf.lfPIob').get_text()
            data = [title, ]

            addr_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png'
            phone_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png'
            website_img_src = '//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png'

            for img_src in (addr_img_src, phone_img_src, website_img_src):
                img_element = soup.select_one(f'img[src="{img_src}"]')
                info = img_element.parent.parent.parent.select_one('.Io6YTe').get_text() \
                    if img_element else '-'
                data.append(info)

            return data

        entries = []
        for url in urls:
            await self._open_url_and_wait(url)
            html = await self.page.content()
            data = parse_data_with_soup(html)
            entries.append(dict(zip(self.FIELD_NAMES, data)))

        return entries
