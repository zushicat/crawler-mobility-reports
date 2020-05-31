import os

from _request_apple import request_apple
from _request_google import request_google
from _request_rki import request_rki

import click


@click.command()
@click.option('--all', 'requested_source', default=True, flag_value='all', help='Request all sources')
@click.option('--apple', 'requested_source', default=False, flag_value='apple', help='Request Apple')
@click.option('--google', 'requested_source', default=False, flag_value='google', help='Request Google')
@click.option('--rki', 'requested_source', default=False, flag_value='rki', help='Request RIK')
def request_sources(requested_source):
    '''
    Request sources by options
    '''
    functions = {
        "apple": request_apple,
        "google": request_google,
        "rki": request_rki,
    }

    if requested_source == "all":
        for fkt in functions.values():
            try:
                fkt()
            except Exception as e:
                print(f"ERROR -------> {e}")
    else:
        functions[requested_source]()
   
if __name__ == '__main__':
    request_sources()
