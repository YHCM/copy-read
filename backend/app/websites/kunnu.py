import httpx
from parsel import Selector
from starlette import status

from app.schemas import TempBook, TempChapter
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
        self.client = httpx.Client(headers=self.headers)

    def get_domain(self) -> str:
        return self.domain

    def search(self, keyword: str) -> list[TempBook]:
        results = []

        response = self.client.get(f"https://www.kunnu.com/?s={keyword}")
        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            url_results = selector.xpath(
                '//li[@class="cat-search-item"]/a/@href'
            ).getall()
            title_results = selector.xpath(
                '//li[@class="cat-search-item"]/a/text()'
            ).getall()

            for url, title in zip(url_results, title_results):
                author = self.get_author(url)

                temp_book = TempBook(
                    book_domain=self.domain,
                    book_title=title,
                    book_url=url,
                    author_name=author,
                )

                results.append(temp_book)
        else:
            # 异常处理，之后做
            pass

        return results

    def get_chapters(self, book_url: str) -> list[TempChapter]:
        results = []

        response = self.client.get(book_url)

        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            chapter_tags = selector.xpath('//div[@class="book-list clearfix"]/ul/li')

            for index, chapter_tag in enumerate(chapter_tags, start=1):
                temp_chapter = None

                # 处理 <a> 标签
                a_tag = chapter_tag.xpath("./a")
                if a_tag:
                    title = a_tag.xpath("./text()").get(default="")
                    url = a_tag.xpath("./@href").get(default="")
                    temp_chapter = TempChapter(
                        book_url=book_url,
                        chapter_id=index,
                        chapter_title=title,
                        chapter_url=url,
                    )

                # 处理 <b> 标签
                b_tag = chapter_tag.xpath("./b")
                if b_tag:
                    title = b_tag.xpath("./text()").get(default="")
                    url = b_tag.xpath("./@onclick").re(r"window\.open\('(.*?)'\)")[0]
                    temp_chapter = TempChapter(
                        book_url=book_url,
                        chapter_id=index,
                        chapter_title=title,
                        chapter_url=url,
                    )

                results.append(temp_chapter)
        else:
            # 异常处理，之后做
            pass

        return results

    def get_content(self, chapter_url: str) -> str:
        result = ""

        response = self.client.get(chapter_url)

        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            # 先简单处理一下
            tags = selector.xpath('//div[@id="nr1"]/p').getall()
            result = "".join(tags)
        else:
            pass

        return result

    def get_author(self, book_url: str) -> str:
        """
        获取书的作者

        Args:
            book_url (str): 书籍主页的 url

        Returns:
            str: 书籍作者
        """
        response = self.client.get(book_url)

        author = ""
        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            text = selector.xpath('//div[@class="book-describe"]/p[1]/text()').get(
                default=""
            )
            author = text.strip().split("：")[1] if "：" in text else ""
        else:
            # 异常处理，之后做
            pass

        return author


if __name__ == "__main__":
    kunnu = KunNu()
    # result = kunnu.get_author("https://www.kunnu.com/xusanguanmaixueji/")
    results = kunnu.get_content("https://www.kunnu.com/wanmei/9.htm")
    print(results)
