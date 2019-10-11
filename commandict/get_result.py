#!/usr/bin/env python
""" get_result.py """

import click
from urllib.parse import parse_qsl, urlparse

import requests
from bs4 import BeautifulSoup


DAUM_DICT_HOST = "https://alldic.daum.net/"

LANG = 'eng'

COMMAND_SET = {
    'a': 'antonym',
    's': 'synonym',
    'q': 'quit'
}


COMMANDS = "more: " + ' | '.join(
    [f'{COMMAND_SET[key]}({key})' for key in COMMAND_SET]
)


def parse(html: str):
    bs = BeautifulSoup(html, 'html.parser')
    content = bs.findAll('meta', attrs={'property': 'og:description'})[0]\
        .get('content')
    try:
        redir_url = bs.findAll('meta', attrs={'http-equiv': 'Refresh'})[0]\
            .get('content').split('URL=')[1]
    except IndexError:
        # the result comes with polysemic words
        redir_url = bs.findAll('a', attrs={'txt_cleansch'})[0].attrs['href']
    dic_query = urlparse(redir_url).query
    wordid = dict(parse_qsl(dic_query))['wordid']
    return content, wordid


def parse_detail(html: str, wordid: str, category: str):
    """ parse once more to get the detailed view """

    bs = BeautifulSoup(html, 'html.parser')

    id_set = {
        'antonym': 'OPPOSITE_WORD',
        'synonym': 'SIMILAR_WORD'
    }
    if category not in id_set.keys():
        pass
    else:
        words = bs.find(id=id_set[category])
        if not words:
            # there's no antonym of this keyword
            return 'No results found.'
        tags = words.findAll('li')
        result = [
            f"{tag.find('a').text}: {tag.find('span').text}" for tag in tags
        ]
        return '\n'.join(result)


@click.command()
@click.argument('keyword')
def main(keyword):
    click.echo('Searching...')
    url = f'{DAUM_DICT_HOST}search.do?q={keyword}&dic={LANG}'
    response = requests.get(url)
    meanings, wordid = parse(response.text)
    detailed_url = f'https://dic.daum.net/word/view.do?wordid={wordid}'
    detailed_text = None
    click.echo(meanings)

    while(True):
        value = click.prompt(click.style(COMMANDS, fg='white', bg='blue'))
        command = COMMAND_SET[value]

        if value != 'q':
            if detailed_text is None:
                detailed_text = requests.get(detailed_url).text

            result = parse_detail(detailed_text, wordid, command)
            click.secho(command, fg='green')
            click.echo(result)
        else:
            break


if __name__ == "__main__":
    main()
