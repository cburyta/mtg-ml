import click
from copy import copy
import json
from psycopg2 import OperationalError
from postgres import Postgres
from preprocessor.card_preprocessor import CardOracleTextProcessor

db_url = "postgres://mtg:mtg_pass@localhost:5432/mtg_local"

@click.group()
def mtg_ml():
    pass

@mtg_ml.command()
def preprocess():
    '''Command on mtg_ml'''
    batchsize = 1000
    processor_limit = 5
    click.echo(f'Running preprocessor on card oracle text in batches of {batchsize} and a process limit of {processor_limit}')
    processor = CardOracleTextProcessor(db_url=db_url, batchsize=1000, processor_limit=5)
    processor.process_all_cards()


@mtg_ml.command()
def cmd2():
    '''Command on mtg_ml'''
    click.echo('mtg_ml cmd2')

if __name__ == '__main__':
    mtg_ml()
