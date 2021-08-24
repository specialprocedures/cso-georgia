import scrapy
import requests
from math import ceil


class MySpider(scrapy.Spider):
    name = "company_spider"
    allowed_domains = ["api.companyinfo.ge"]
    base_url = "https://api.companyinfo.ge/api/corporations/"

    def start_requests(self):
        search_url = self.base_url + "search?legalForm=7"

        initial_request = requests.get(search_url).json()
        total_items = initial_request["totalItems"]
        total_pages = ceil(total_items / initial_request["itemPerPage"])

        start_urls = [f"{search_url}&page={i}" for i in range(1, total_pages + 1)]

        for url in start_urls:
            yield scrapy.Request(url, self.parse)

    def parse(self, response):

        for item in response.json()["items"]:
            url = self.base_url + str(item["id"])
            yield scrapy.Request(url, self.parse_company)

    def parse_company(self, response):
        item = response.json()
        yield item
