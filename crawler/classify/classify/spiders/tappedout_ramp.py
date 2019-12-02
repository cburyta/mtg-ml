# -*- coding: utf-8 -*-
import scrapy

from classify.items import CardItem
from classify.loaders import CardLoader


class TappedoutRampSpider(scrapy.Spider):
    name = 'tappedout_ramp'
    allowed_domains = ['tappedout.com']
    start_urls = ['http://tappedout.net/mtg-decks/list-of-edh-ramp-cards/']

    def parse(self, response):
        for card in response.css('.board-container ul li a.card-link'):

            # build a list of decks
            l = CardLoader(item=CardItem(), selector=card)
            l.add_value('name', card.attrib['data-name'])
            l.add_value('card_type', 'ramp')

            card_item = l.load_item()

            # print('CARD: Name: %s, Type: %s' % (card_item['name'], card_item['card_type']))

            yield card_item
