from abc import ABC


class AbstractEngine(ABC):
    '''
    `AbstractEngine`

    Abstract class specifying main methods and attributes
    '''
    BASE_URL = ''
    FIELD_NAMES = []

    def __init__(self, *args, **kwargs) -> None:
        '''
        Initializer method
        '''
        pass

    async def run(self, *args, **kwargs) -> None:
        '''
        Main method to run the engine
        '''
        pass

    async def _get_search_results_urls(self, *args, **kwargs) -> list[str]:
        '''
        Retreiving search results URLs from the website (Yelp/Google Maps) method
        '''
        pass

    async def _get_search_results_entries(self, urls: list[str], *args, **kwargs) -> list[dict]:
        '''
        Retreiving search results data entries method from urls
        '''
        pass
