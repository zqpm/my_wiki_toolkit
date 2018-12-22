#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

postfix = ' release'  # This is used for creating new wiki page.

doc_options = [
    # 'no' is a reminder to make sure how many documents should be generated.
    # 'title' will be the name of pdf file. And the new generated wiki page will
    # be 'title'+postfix.
    # 'content': If not empty, program will merge these pages into a new page.
    # Ex:
    # postfix = ' append'
    # doc_options = [
    #    {
    #          'no': '1',
    #          'title': 'testpage',
    #          'content': [
    #              'page1',
    #              'page2',
    #          ]
    #     }
    # ]
    # The program will create a new page 'testpage append' and the contents are
    # page1 and page2.
    {
        'no': '1',
        'title': '',
        'content': []
    }
]
