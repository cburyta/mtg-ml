import click

@click.group()
def mtg_ml():
    pass

@mtg_ml.command()
def cmd1():
    '''Command on mtg_ml'''
    click.echo('mtg_ml cmd1')

@mtg_ml.command()
def cmd2():
    '''Command on mtg_ml'''
    click.echo('mtg_ml cmd2')

if __name__ == '__main__':
    mtg_ml()
