from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose


class PageItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    content_in = MapCompose()
    url_in = MapCompose()
