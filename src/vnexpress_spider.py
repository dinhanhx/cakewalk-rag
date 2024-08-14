import scrapy


class VnexpressSpider(scrapy.Spider):
    name = "vnexpress"
    start_urls = ["https://vnexpress.net/giao-duc/tin-tuc"]

    def parse(self, response):
        for i in response.css(".col-left-new .title-news a"):
            yield response.follow(i, callback=self.parse_article)

    def parse_article(self, response):
        """ This only get plain text, not tables or images. """
        link = response.url
        title = response.css(".title-detail::text").get()
        description = response.css(".description::text").get()
        paragraphs = response.css(".fck_detail p::text").getall()
        yield {
            "link": link,
            "title": title,
            "content": [description, *paragraphs]
        }
