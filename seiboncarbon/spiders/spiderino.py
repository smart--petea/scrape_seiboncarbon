from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy import log
from seiboncarbon.items import SeiboncarbonItem
from scrapy.selector import HtmlXPathSelector
import re

#My re
reImageUrl = re.compile(r'src="(.*?)"')
rePrice = re.compile(r'class="price">\$(.*?)<')
reProdName = re.compile(r'class="product-essential">.*?>(.*?)<', re.DOTALL)
reBreadCrumb = re.compile(r'>(.*?)<')
reProperties = re.compile(r'class="label">(.*?)<.*?class="data">(.*?)<', re.DOTALL)
reProdPage = re.compile(r'class="product-name".*?href="(.*?)"')
reCategory = re.compile(r'"(http://.*?product_category=.*?)"')

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SpiderIno(BaseSpider):

	name = 'carbon'
	
	def start_requests(self):
		yield Request('http://seiboncarbon.com/store/products.html', callback = self.parse_For_category)

	def parse_For_category(self, response):
		MyCategories = reCategory.findall(response.body)
		for category in MyCategories:
			yield Request(category, callback=self.parse_category)
		
	def parse_category(self, response):
		ProdLinks = reProdPage.findall(response.body)
		for link in ProdLinks:
			yield Request(link, callback=self.parse_page)

	def parse_page(self, response):
		print('am primit: ', response.url)
		MySel = HtmlXPathSelector(response)
		item = SeiboncarbonItem()
		#breadcrumbs
		m = MySel.select('//div[@class="breadcrumbs"]/ul')[0].extract()
		m = reBreadCrumb.findall(m)
		item['BreadCrumb'] = ">>".join([x for x in m if '&gt' not in x]).strip('>')
		
		#image urls
		try:
			m = MySel.select('//div[@class="more-views"]')[0].extract()
		except IndexError:
			m = ''
		
		MyList = reImageUrl.findall(m)
		item['image_urls'] = MyList

		prod_image = MySel.select('//p[@class="product-image"]/a/@href')[0].extract()
		item['image_urls'].append(prod_image) #the last image is the principal
		item['Price'] = rePrice.search(response.body).group(1)

		#Product Name
		item['ProductName'] = reProdName.search(response.body).group(1)

		#description
		try:
			item['MetaDesc'] = MySel.select('//div[@class="std"]')[0].extract()
		except IndexError:
			item['MetaDesc'] = ''

		#properties
		m = reProperties.findall(response.body)
		if m: #if m != []
			item['Properties'] = {''.join(x[0].split()): x[1] for x in m}

		yield item
			
