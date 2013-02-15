# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SeiboncarbonItem(Item):
	BreadCrumb = Field()
	image_urls = Field()
	images = Field()
	Price = Field()
	MetaDesc = Field()
	ProductName = Field()
	Properties = Field()
