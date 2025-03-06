import httpx
from parsel import Selector

from app.models import BookInfo
from app.schemas import ChapterInfo
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
        self.client = httpx.AsyncClient(headers=self.headers, timeout=None)

    def get_domain(self) -> str:
        return self.domain

    async def search(self, keyword: str) -> list[BookInfo]:
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
                author = await self.__get_author(url)

                book_info = BookInfo(
                    book_domain=self.domain,
                    book_url=url,
                    book_name=name,
                    book_author=author,
                )
                results.append(book_info)

        else:
            # 异常处理，之后做
            pass

        return results

    async def get_chapter_info(self, book_url: str) -> list[ChapterInfo]:
        results = []

        response = await self.client.get(book_url)

        if response.status_code == 200:
            selector = Selector(response.text)
            chapters = selector.xpath('//div[@class="book-list clearfix"]/ul/li')

            for index, chapter in enumerate(chapters, start=1):
                chapter_info = None

                # 处理 <a> 标签形式
                a_tag = chapter.xpath("./a")
                if a_tag:
                    title = a_tag.xpath("./text()").get(default="")
                    url = a_tag.xpath("./@href").get(default="")
                    chapter_info = ChapterInfo(
                        chapter_id=index, chapter_url=url, chapter_title=title
                    )

                # 处理 <b> 标签形式
                b_tag = chapter.xpath("./b")
                if b_tag:
                    title = b_tag.xpath("./text()").get(default="")
                    url = b_tag.xpath("./@onclick").re(r"window\.open\('(.*?)'\)")[0]
                    chapter_info = ChapterInfo(
                        chapter_id=index, chapter_url=url, chapter_title=title
                    )

                results.append(chapter_info)
        else:
            pass

        return results

    async def __get_author(self, book_url) -> str:
        response = await self.client.get(book_url)

        author = ""

        if response.status_code == 200:
            selector = Selector(response.text)
            text = selector.xpath('//div[@class="book-describe"]/p[1]/text()').get()

            if text:
                author = text.strip().split("：")[1] if "：" in text else ""
        else:
            # 异常处理，以后做
            pass

        return author


if __name__ == "__main__":
    import asyncio

    kunnu = KunNu()

    chapters = asyncio.run(
        kunnu.get_chapter_info("https://www.kunnu.com/xusanguanmaixueji/")
    )

    print(chapters)
