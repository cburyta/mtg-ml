from multiprocessing import Process
import os
import math
import json
from copy import copy
from postgres import Postgres
from nlp.oracle_text_parser import OracleTextParser


class CardProcessorProcess(Process):
    def __init__(self, cards, db_url):
        super().__init__()
        self.db = Postgres(url=db_url)
        self.cards = cards

    def info(self, msg):
        print(f'card processor process {os.getpid()}: {msg}')

    def _insert_card_cost_and_effect(self, card_id, cost, effect):
        self.db.run(
            f"INSERT INTO actions(card_id, cost, effect) VALUES(%(card_id)s, %(action_cost)s, %(action_effect)s)",
            {'card_id': card_id, 'action_cost': cost, 'action_effect': effect})

    def get_parsed_oracle_text_from_card(self, card):
        oracle_text = card.oracle_text
        if oracle_text is None:
            oracle_text = ''
        return OracleTextParser.parse_oracle_text(oracle_text)

    def parse_and_save_card_in_db(self, card):
        parsed_oracle_text = self.get_parsed_oracle_text_from_card(card)
        card_id = card.id
        for action in parsed_oracle_text:
            action_cost = json.dumps(str(action['cost']))
            action_effect = json.dumps(str(action['effect']))
            self._insert_card_cost_and_effect(card_id, action_cost, action_effect)

    def run(self):
        cards = self.cards
        self.info('Extracting cost and effect from each card and writing to db')
        for card_index in range(len(cards)):
            if card_index % 100 == 0: # throttle progress report from thread
                self.info(f'{math.floor((card_index / 1000) * 100)}%')
            card = cards[card_index]
            self.parse_and_save_card_in_db(card)


class CardOracleTextProcessor:
    def __init__(self, db_url, batchsize=1000, processor_limit = 5):
        self.db_url = db_url
        self.db = Postgres(url=db_url)
        self.batchsize = batchsize
        self.processor_limit = processor_limit
        self.process_count = 0
        self.processors = []
        self.offset = 0

    def get_all_cards_from_db(self):
        return self.db.all(f"select id,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en' limit {self.batchsize}")

    def get_all_cards_from_db_with_offset(self):
        return self.db.all(f"select id,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en' limit {self.batchsize} offset {self.offset}")

    def limit_processes(self):
        if len(self.processors) % self.processor_limit == 0:
            print('waiting for processing jobs to finish')
            for processor in self.processors:
                processor.join()
                print(f'{processor.name} finished.')
            self.processors = []

    def setup_and_start_card_processor_process(self, cards):
        cards_copy = copy(cards)
        card_preprocessor = CardProcessorProcess(cards=cards_copy, db_url=self.db_url)
        card_preprocessor.start()
        self.processors.append(card_preprocessor)
        return card_preprocessor

    def process_all_cards(self):
        print(f"Pulling first batch of {self.batchsize} cards from database")
        cards = self.get_all_cards_from_db()

        while len(cards):
            self.offset += 1
            self.limit_processes()
            print('setting up card processing thread')
            self.setup_and_start_card_processor_process(cards)
            print(f"Pulling next 1000 cards (batch #{self.offset})")
            cards = self.get_all_cards_from_db_with_offset()
