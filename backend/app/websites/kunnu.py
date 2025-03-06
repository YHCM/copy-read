import httpx
from parsel import Selector

from app.models import BookInfo
from app.websites.site import Site


class KunNu(Site):
    def __init__(self) -> None:
        self.domain = "www.kunnu.com"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Priority": "u=0, i",
            "Referer": "https://www.kunnu.com/",
            "Sec-CH-UA": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        }
        self.client = httpx.AsyncClient(headers=self.headers)

    def get_domain(self) -> str:
        return self.domain

    async def search(self, keyword: str) -> list[BookInfo]:
        """
        www.kunnu.com 的搜索 api

        Args:
            keyword (str): 搜索关键字

        Returns:
            list[BookInfo]: 搜索结果
        """
        results = []

        response = await self.client.get(f"https://www.kunnu.com/?s={keyword}")
        if response.status_code == 200:
            selector = Selector(response.text)
            url_results = selector.xpath(
                '//li[@class="cat-search-item"]/a/@href'
            ).getall()
            name_results = selector.xpath(
                '//li[@class="cat-search-item"]/a/text()'
            ).getall()

            for url, name in zip(url_results, name_results):
                book_info = BookInfo(
                    book_domain=self.domain, book_url=url, book_name=name
                )
                results.append(book_info)

        else:
            # 异常处理，之后做
            pass

        return results
