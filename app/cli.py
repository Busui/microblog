from app import app
import os
import click


@app.cli.group()
def translate():
    """Translate and localization commands."""
    pass


@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('Extract command faild')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command faild.')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command faild')


@translate.command()
@click.argument('lang')
def init(lang):
    """Initilize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('Extract command failed')
    if os.system('pytabel init -i messages.pot -d app/translates -l' + lang):
        raise RuntimeError('init command faild')
    os.remove('messages.pot')