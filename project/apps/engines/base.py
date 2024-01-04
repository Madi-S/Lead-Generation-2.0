import asyncio

from apps.misc.writer import CsvWriter


class BaseEngine:
    def save_to_csv(self, filename: str = 'google_maps_leads.csv') -> None:
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

    async def _open_url_and_wait(self, url: str, sleep_duration_s: int = 3) -> None:
        '''
        `url: str` - url to open
        `sleep_duration_s: int = 3` - amount of seconds to wait for the page to load before any operations on that page

        Navigates to initialized `self.url` and waits for `sleep_duration_s` seconds
        '''
        await self.page.goto(url)
        await asyncio.sleep(sleep_duration_s)
