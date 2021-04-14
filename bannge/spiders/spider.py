import scrapy

from scrapy.loader import ItemLoader

from ..items import BanngeItem
from itemloaders.processors import TakeFirst


class BanngeSpider(scrapy.Spider):
	name = 'bannge'
	start_urls = ['http://www.bannge.com/en/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="more-link secondary-color"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="entry-title"]/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=BanngeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
