import time
import asyncio
from bs4 import BeautifulSoup

from apps.engines.base import BaseEngine
from apps.engines.abstract import AbstractEngine


class YelpEngine(BaseEngine, AbstractEngine):
    '''
    `YelpEngine`

    Usage:

    `engine = YelpEngine(*args, **kwargs)`

    `await engine.run()`

    `await engine.save_to_csv()`

    `print(engine.entries)`
    '''
    BASE_URL = 'https://www.yelp.com/search?find_desc={query}&find_loc={location}%2C+Philippines&start=0'
    # https://www.yelp.com/search?find_desc=pizza&find_loc=Mexico%2C+Pampanga%2C+Philippines&start=0
    FIELD_NAMES = ['Title', 'Address', 'PhoneNumber', 'Tags']

    def __init__(self, query: str, location: str) -> None:
        '''
        '''
        self._entries = []
        self.query = query
        self.location = location
        self.url = self.BASE_URL.format(
            query=self.query, location=self.location
        )

    async def _get_search_results_urls(self) -> list[str]:
        '''
        '''
        urls = []
        host = 'https://www.yelp.com'
        while True:
            await asyncio.sleep(3)
            link_elements = await self.page.query_selector_all('.css-1hqkluu')
            for link_element in link_elements:
                url = await link_element.get_attribute('href')
                url = host + url
                urls.append(url)

            next_page_btn = await self.page.query_selector(
                '.next-link.navigation-button__09f24__m9qRz.css-ahgoya'
            )
            if not next_page_btn:
                break

            await next_page_btn.scroll_into_view_if_needed()
            await next_page_btn.click()

        return urls

    async def _get_search_results_entries(self, urls: list[str]) -> list[dict]:
        ''''''
        # TODO: move this piece of code to BaseEngine

        def parse_data_with_soup(html: str) -> list:
            soup = BeautifulSoup(html, 'html.parser')
            data = []

            title = soup.select_one('.css-1se8maq').get_text()
            data.append(title)

            addr = soup.select_one('.css-qyp8bo').get_text()
            data.append(addr)

            phone = soup.select_one('.css-djo2w .css-1p9ibgf').get_text()
            data.append(phone)

            tags = []
            tag_elements = soup.select('.css-1xfc281 span.css-1fdy0l5')
            for tag_element in tag_elements:
                tag = tag_element.find('a').get_text()
                tags.append(tag)

            data.append(','.join(tags))

            return data

        entries = []
        for url in urls:
            await self._open_url_and_wait(url, 1.5)
            html = await self.page.content()
            data = parse_data_with_soup(html)
            entry = dict(zip(self.FIELD_NAMES, data))
            entries.append(entry)
            print(entry)

        return entries
