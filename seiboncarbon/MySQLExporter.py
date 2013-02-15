import MySQLdb
from scrapy import log
from scrapy import signals
from scrapy.exceptions import NotConfigured, DropItem

class MySQLExporter(object):
	def __init__(self, mysqlConnection):
		self.connection = mysqlConnection
		self.cursor = mysqlConnection.cursor()
		log.msg(message="MySQLExporter - initiate", _level = log.INFO)

	@classmethod
	def from_crawler(cls, crawler):
		user = crawler.settings.get('MySQLUser', 'root')
		passwd = crawler.settings.get('MySQLPassw', 'kate')
		host = crawler.settings.get('MySQLHost', 'localhost')
		db = crawler.settings.get('MySQLdb', 'kino')
		mysqlConnection = MySQLdb.connect(host = host, user = user, passwd = passwd, db= db)
		cls = cls(mysqlConnection)
		crawler.signals.connect(cls.item_scraped, signal = signals.item_scraped)

		return cls

	def item_scraped(self, item, spider):
		try:
			properties = item['Properties']
			years =  properties.get('Year', None)
			if years:
				list_years = years.split()
				len_list = len(list_years)
				if len_list == 1:
					LastYear = FirstYear = list_years[0].strip(',')
				else:
					LastYear = list_years[0].strip(',')
					FirstYear = list_years[1].strip(',')
			else:
				LastYear = FirstYear = ''

			self.cursor.execute("INSERT INTO main(ProductName, BreadCrumb, Price, MetaDesc, Sku, Year, Make, Model, BodyType, Chassis, CarbonType, ProductCategory, SpecialNotes, LastYear, FirstYear) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (item['ProductName'],
				item['BreadCrumb'], item['Price'], item['MetaDesc'],
				properties.get('SKU', ''), properties.get('Year', ''), properties.get('Make', ''),
				properties.get('Model', ''), properties.get('BodyType', ''), properties.get('Chassis', ''),
				properties.get('CarbonType', ''), properties.get('ProductCategory', ''), properties.get('SpecialNotes', ''), LastYear, FirstYear))


			#images
			MyImages = [(item['ProductName'], 'image' if 'image' in x['url'] else 'more-views',MySQLdb.escape_string(open('MyImage/' + x['path'], 'rb').read())) for x in item['images']]
			self.cursor.executemany('INSERT INTO image(ProductName, Type, Content) Values(%s, %s, %s)', MyImages)


		except Exception as e:
			print(e)
			return DropItem

		else:
			self.connection.commit()
			return item
