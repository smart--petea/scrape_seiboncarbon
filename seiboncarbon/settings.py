# Scrapy settings for seiboncarbon project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'seiboncarbon'

SPIDER_MODULES = ['seiboncarbon.spiders.spiderino']
NEWSPIDER_MODULE = 'seiboncarbon.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.57 Safari/537.17'
LOG_FILE = 'crawl.log'
CLOSESPIDER_ITEMCOUNT = 2001
CONCURRENT_REQUESTS_PER_IP = 6

DOWNLOAD_DELAY = 0.25

IMAGES_STORE = 'MyImage'
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']


MySQLUser = 'root'
MySQLPassw = 'kate'
MySQLHost = 'localhost'
MySQLdb = 'seibon'

EXTENSIONS = {'seiboncarbon.MySQLExporter.MySQLExporter': 500}
