from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class CardLoader(ItemLoader):
  default_output_processor = TakeFirst()

