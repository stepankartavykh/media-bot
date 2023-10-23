import requests
import aiohttp


class RequestHandler:
    def __init__(self, url):
        self.url = url
        default_headers = requests.utils.default_headers()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        default_headers.update({'User-Agent': user_agent})
        self.headers = default_headers

    async def make_request(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url, headers=self.headers) as response:
                html = await response.text()
                return html
        # return await requests.get(self.url, headers=self.headers).text
