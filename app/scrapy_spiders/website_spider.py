from typing import Any
import scrapy

class WebsiteSpider(scrapy.Spider):
    name="website_spider"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url] if start_url else []

    def parse(self, response):
        # Get full HTML as string
        html_content = response.text
        yield {"html": html_content}