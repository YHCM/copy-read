import httpx
from parsel import Selector

from app.models import BookInfo
from app.schemas import ChapterInfo
from app.websites.site import Site


class SuDuGu(Site):
    def __init__(self) -> None:
        self.domain = "www.sudugu.com"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Connection": "keep-alive",
            "Host": "www.sudugu.com",
            # "Referer": "https://www.sudugu.com/i/so.aspx",
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
        results = []

        # 更新请求头，将 Referer 更新为搜索页面
        search_referer = {"Referer": "https://www.sudugu.com/i/so.aspx"}
        self.headers.update(search_referer)

        response = await self.client.get(
            f"https://www.sudugu.com/i/sor.aspx?key={keyword}", headers=self.headers
        )

        if response.status_code == 200:
            selector = Selector(response.text)
            url_results = selector.xpath('//div[@class="item"]/div/h3/a/@href').getall()
            name_results = selector.xpath(
                '//div[@class="item"]/div/h3/a/text()'
            ).getall()
            author_results = selector.xpath(
                '//div[@class="item"]/div/p[2]/a/text()'
            ).getall()

            for url, name, author in zip(url_results, name_results, author_results):
                full_url = f"https://www.sudugu.com{url}"
                book_author = author.strip().split("：")[1] if "：" in author else ""
                book_info = BookInfo(
                    book_domain=self.domain,
                    book_url=full_url,
                    book_name=name,
                    book_author=book_author,
                )
                results.append(book_info)

        else:
            # 异常处理，之后做
            pass

        return results

    async def get_chapter_info(self, book_url: str) -> list[ChapterInfo]:
        results = []

        # 更新请求头，将 Referer 更新为搜索页面
        search_referer = {"Referer": "https://www.sudugu.com/"}
        self.headers.update(search_referer)
        response = await self.client.get(book_url)

        if response.status_code == 200:
            selector = Selector(response.text)
            chapters = selector.xpath('//div[@id="list"]/ul/li')

            for index, chapter in enumerate(chapters, start=1):
                url = chapter.xpath("./a/@href").get(default="")
                title = chapter.xpath("./a/text()").get(default="")
                full_url = f"https://www.sudugu.com{url}"
                chapter_info = ChapterInfo(
                    chapter_id=index, chapter_url=full_url, chapter_title=title
                )
                results.append(chapter_info)
        else:
            pass

        return results


if __name__ == "__main__":
    import asyncio

    sudugu = SuDuGu()

    chapters = asyncio.run(sudugu.get_chapter_info("https://www.sudugu.com/1637/"))
    print(chapters)
