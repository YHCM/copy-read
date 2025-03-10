import httpx
from parsel import Selector
from starlette import status

from app.schemas import TempBook, TempChapter
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
        self.client = httpx.Client()

    def get_domain(self):
        return self.domain

    def search(self, keyword: str) -> list[TempBook]:
        results = []

        # 更新请求头，将 Referer 更新为搜索页面
        search_referer = {"Referer": "https://www.sudugu.com/i/so.aspx"}
        self.headers.update(search_referer)

        response = self.client.get(
            f"https://www.sudugu.com/i/sor.aspx?key={keyword}", headers=self.headers
        )

        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            url_results = selector.xpath('//div[@class="item"]/div/h3/a/@href').getall()
            title_results = selector.xpath(
                '//div[@class="item"]/div/h3/a/text()'
            ).getall()
            author_results = selector.xpath(
                '//div[@class="item"]/div/p[2]/a/text()'
            ).getall()

            for url, title, author in zip(url_results, title_results, author_results):
                full_url = f"https://www.sudugu.com{url}"
                author_name = author.strip().split("：")[1] if "：" in author else ""

                temp_book = TempBook(
                    book_domain=self.domain,
                    book_title=title,
                    book_url=full_url,
                    author_name=author_name,
                )

                results.append(temp_book)
        else:
            # 异常处理，之后做
            pass

        return results

    def get_chapters(self, book_url: str) -> list[TempChapter]:
        results = []

        # 更新请求头，将 Referer 更新为主页
        search_referer = {"Referer": "https://www.sudugu.com/"}
        self.headers.update(search_referer)
        response = self.client.get(book_url, headers=self.headers)

        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)
            chapter_tags = selector.xpath('//div[@id="list"]/ul/li')

            for index, chapter_tag in enumerate(chapter_tags, start=1):
                url = chapter_tag.xpath("./a/@href").get(default="")
                title = chapter_tag.xpath("./a/text()").get(default="")
                full_url = f"https://www.sudugu.com{url}"

                temp_chapter = TempChapter(
                    book_url=book_url,
                    chapter_id=index,
                    chapter_title=title,
                    chapter_url=full_url,
                )

                results.append(temp_chapter)
        else:
            # 异常处理，之后做
            pass

        return results

    def get_content(self, chapter_url: str) -> str:
        book_url = chapter_url[: chapter_url.rfind("/")] + "/"

        return self.get_page_content(book_url, chapter_url)

    def get_page_content(self, referer_url: str, chapter_url: str) -> str:
        # 更新请求头，将 Referer 更新为上一页
        referer = {"Referer": referer_url}
        self.headers.update(referer)

        response = self.client.get(chapter_url, headers=self.headers)
        if response.status_code == status.HTTP_200_OK:
            selector = Selector(response.text)

            # 提取页面的内容
            tags = selector.xpath('//div[@class="con"]/p').getall()
            content = "".join(tags)

            # 获取下一页的链接
            next_tag = selector.xpath('//div[@class="prenext"]/span[2]/a')
            next_url = next_tag.xpath("./@href").get(default="")
            next_url = f"https://www.sudugu.com/{next_url}"
            next_text = next_tag.xpath("./text()").get(default="")

            # 如果有下一页，递归获取
            if next_text == "下一页":
                content += self.get_page_content(chapter_url, next_url)

            return content

        return ""


if __name__ == "__main__":
    sudugu = SuDuGu()
    results = sudugu.get_content("https://www.sudugu.com/651/983354.html")
    print(results)
