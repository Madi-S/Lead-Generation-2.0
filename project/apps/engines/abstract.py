from abc import ABC


class AbstractEngine(ABC):
    '''
    `AbstractEngine`

    Abstract class specifying main methods and attributes

    [CONSTANT] `BASE_URL` - base url for google maps website with substitute search query, coordinates and zoom 

    [CONSTANT] `FIELD_NAMES` - field names of scraped data, extracts data entries to csv file based on these field names
    '''

    BASE_URL = ''
    FIELD_NAMES = []

    async def _get_search_results_urls(self, *args, **kwargs) -> list[str]:
        '''
        Retreiving search results URLs from the website (Yelp/Google Maps) method
        '''
        pass

    def _parse_data_with_soup(self, html):
        '''
        `html: str` - html representation of the page to parse

        Should be defined in child class

        Returns `list[dict]` typed parsed data - `[title, addr, phone, website]`
        '''
        pass
