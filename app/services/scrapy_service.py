from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher
from scrapy import signals
from multiprocessing import Queue
import os
import sys
from ..scrapy_spiders.website_spider import WebsiteSpider

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scrapy_spiders")))

html_output = {}

def catch_item(sender, item, **kwargs):
    html_output['html'] = item['html']

def scrape_url(url: str) -> str:
    dispatcher.connect(catch_item, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(WebsiteSpider, start_url=url)
    process.start()

    return html_output.get('html', "")


