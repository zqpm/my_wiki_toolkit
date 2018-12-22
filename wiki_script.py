#!/usr/bin/python2.7
# -*- coding: utf-8 -*- 

# TODO: Use dict.get to replace direct access.

import sys

from wikitools.wiki import Wiki

from configs.wiki_config import src_wiki_options, dest_wiki_options
from basic_sdk import Logger


if __name__ == '__main__':
    log = Logger('wiki_operation_script.log')

    try:
        src_wiki = Wiki(src_wiki_options['web_api'])
        dest_wiki = Wiki(dest_wiki_options['web_api'])
        result1 = src_wiki.login(username=src_wiki_options['username'],
                                 password=src_wiki_options['password'],
                                 domain=src_wiki_options['domain'])
        result2 = dest_wiki.login(username=dest_wiki_options['username'],
                                  password=dest_wiki_options['password'],
                                  domain=dest_wiki_options['domain'])
    except KeyError:
        log.critical('Something wrong in wiki configurations.')
        sys.exit(1)

    if not result1 or not result2:
        print('Login failed, please check username, password or domain name.')
        sys.exit(1)

    src_wiki.logout()
    dest_wiki.logout()

    sys.exit(0)
