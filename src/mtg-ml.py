import click
from copy import copy
import sys
from nlp.oracle_text_parser import OracleTextParser
from postgres import Postgres
from multiprocessing import Process
import json
import os
import math
from psycopg2 import OperationalError

db_url = "postgres://mtg:mtg_pass@localhost:5432/mtg_local"

def info(msg):
    print(f'process {os.getpid()}: {msg}')

def saveParsedOracleTextToCardInDb(parsed_oracle_text, card_id, db):
    for action in parsed_oracle_text:
        action_cost = json.dumps(str(action['cost']))
        action_effect = json.dumps(str(action['effect']))
        db.run(f"INSERT INTO actions(card_id, cost, effect) VALUES(%(card_id)s, %(action_cost)s, %(action_effect)s)", {'card_id': card_id, 'action_cost': action_cost, 'action_effect':action_effect})

def CardPreprocessor(cards):
    info('Extracting cost and effect from each card and writing to db')
    db = Postgres(url=db_url)
    for card_index in range(len(cards)):
        if card_index % 10 == 0:
            info(f'{math.floor((card_index/1000)*100)}%')
        card = cards[card_index]
        oracle_text = card.oracle_text
        if oracle_text is None:
            oracle_text = ''
        parsed_oracle_text = OracleTextParser.parse_oracle_text(oracle_text)
        saveParsedOracleTextToCardInDb(parsed_oracle_text, card.id, db)
#        except Exception as e:
#            info(f'Crashed on {oracle_text}')
#            sys.exit(1)


@click.group()
def mtg_ml():
    pass

@mtg_ml.command()
def preprocess():
    '''Command on mtg_ml'''
    click.echo('Running preprocessor')
    batchsize = 1000
    processor_limit = 5
    offset = 0
    db = Postgres(url=db_url)
    click.echo(f"Pulling first batch of {batchsize} cards from database")
    cards = db.all(f"select id,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en' limit {batchsize}")
    card_processor_threads = []
    while len(cards):
        offset += 1
        click.echo('setting up card processing thread')
        cards_copy = copy(cards)
        if offset % processor_limit == 0:
            print('waiting for processing jobs to finish')
            for processor in card_processor_threads:
                processor.join()
                print(f'{processor.name} finished.')
            card_processor_threads = []
        card_preprocessor = Process(target=CardPreprocessor, args=(cards_copy,))
        try:
            card_preprocessor.start()
        except OperationalError:
            card_preprocessor.start()
        card_processor_threads.append(card_preprocessor)
        click.echo(f"Pulling next 1000 cards (batch #{offset})")
        cards = db.all(f"select id,oracle_text from cards where exists( select 1 from jsonb_each_text(cards.legalities) j where j.value not like '%not_legal%') and lang='en' limit {batchsize} offset {offset * 1000}")


@mtg_ml.command()
def cmd2():
    '''Command on mtg_ml'''
    click.echo('mtg_ml cmd2')

if __name__ == '__main__':
    mtg_ml()
