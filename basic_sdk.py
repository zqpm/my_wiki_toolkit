#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os
import re
import pdfkit

from wikitools.category import Category
from wikitools.wikifile import File
from wikitools.page import Page

from configs.pdf_config import pdf_options
from configs.sdk_config import log_paths
from configs.wiki_config import src_wiki_options


class WikiMgmt(object):

    def __init__(self):
        self.__log = Logger(log_path=log_paths.get('wikimgmt', 'wikimgmt.log'))

    def copy(self, src_wiki, dest_wiki, category_list=(), page_list=(), image_list=()):
        """
        @summary: This function is used to copy something from source Wiki to destination Wiki.
        @param src_wiki: Source Wiki.
        @param dest_wiki: Destination Wiki.
        @param category_list: List of categories.
        @param page_list: List of pages.
        @param image_list: List of images.
        @return: True for success, False for something failure.
        """
        if not self._check_login_status(src_wiki):
            self.__log.critical('copy: Source Wiki not logged in.')
            return False

        if not self._check_login_status(dest_wiki):
            self.__log.critical('copy: Destination Wiki not logged in.')
            return False

        if not category_list and not page_list and not image_list:
            self.__log.critical('copy: At least specify one.')
            return False

        result = []

        if category_list:
            result.append(self.copy_category(src_wiki, dest_wiki, category_list))

        if page_list:
            result.append(self.copy_page(src_wiki, dest_wiki, page_list))

        if image_list:
            result.append(self.copy_image(src_wiki, dest_wiki, image_list))

        return all(result)

    def copy_category(self, src_wiki, dest_wiki, category_list):
        """
        @summary:
        @param src_wiki:
        @param dest_wiki:
        @param category_list:
        @return:
        """
        if not self._check_login_status(src_wiki):
            self.__log.critical('copy_category: Source Wiki not logged in.')
            return False

        if not self._check_login_status(dest_wiki):
            self.__log.critical('copy_category: Destination Wiki not logged in.')
            return False

        if not isinstance(category_list, list):
            self.__log.critical('delete_page: {0} not list.'.format(category_list))
            return False

        result = []

        for category_title in category_list:
            src_category = Category(src_wiki, title=category_title)
            page_list = src_category.getAllMembers(titleonly=True)

            try:
                result.append(self.copy_page(src_wiki, dest_wiki, page_list))
            except:
                result.append(False)
                self.__log.critical('copy_category: Something went wrong when copy {0}.'.format(page_list))

        result.append(self.copy_page(src_wiki, dest_wiki, page_list=category_list))

        return all(result)

    def copy_page(self, src_wiki, dest_wiki, page_list):
        """
        @summary:
        @param src_wiki:
        @param dest_wiki:
        @param page_list:
        @return:
        """
        if not self._check_login_status(src_wiki):
            self.__log.critical('copy_page: Source Wiki not logged in.')
            return False

        if not self._check_login_status(dest_wiki):
            self.__log.critical('copy_page: Destination Wiki not logged in.')
            return False

        if not isinstance(page_list, list):
            self.__log.critical('copy_page: {0} not list.'.format(page_list))
            return False

        result = []

        for page_title in page_list:
            src_page = Page(src_wiki, title=page_title)

            if not src_page.exists:
                result.append(False)
                self.__log.critical('copy_page: Page {0} not exist.'.format(page_title))
                continue

            dest_page = Page(dest_wiki, title=page_title)
            wiki_text = src_page.getWikiText()

            try:
                result.append(dest_page.edit(wiki_text))
            except:
                result.append(False)
                self.__log.critical('copy_page: Something went wrong when editing destination page {0}.'.format(page_title))

            image_list = self._parse_image_title(wiki_text)
            result.append(self.copy_image(src_wiki, dest_wiki, image_list))

        return all(result)

    def copy_image(self, src_wiki, dest_wiki, image_list):
        """
        @summary:
        @param src_wiki:
        @param dest_wiki:
        @param image_list:
        @return:
        """
        if not self._check_login_status(src_wiki):
            self.__log.critical('copy_image: Source Wiki not logged in.')
            return False

        if not self._check_login_status(dest_wiki):
            self.__log.critical('copy_image: Destination Wiki not logged in.')
            return False

        if not isinstance(image_list, list):
            self.__log.critical('delete_page: {0} not list.'.format(image_list))
            return False

        result = []

        image_url_base = src_wiki_options['image_url']

        for image_title in image_list:
            src_image = File(src_wiki, title=image_title)

            if not src_image.exists:
                result.append(False)
                self.__log.debug('copy_image: Image {0} not exist.'.format(image_title))

            dest_image = File(dest_wiki, title=image_title)

            if dest_image.exists:
                result.append(True)
                self.__log.debug('copy_image: Image {0} already exists.'.format(image_title))

            try:
                full_url = '{0}{1}'.format(image_url_base, src_image.title.split(':')[1].replace(' ', '_'))
                result.append(dest_image.upload(url=full_url, ignorewarnings=True))
            except:
                result.append(False)
                self.__log.critical('copy_image: Something went wrong when copying image {0}.'.format(image_title))

        return all(result)

    def delete(self, wiki, category_list=(), page_list=(), image_list=()):
        if not self._check_login_status(wiki):
            self.__log.critical('delete: wiki not logged in.')
            return False

        if not category_list and not page_list and not image_list:
            self.__log.critical('At least specify one.')
            return False

        result = []

        if category_list:
            result.append(self.delete_category(wiki, category_list))

        if page_list:
            result.append(self.delete_page(wiki, page_list))

        if image_list:
            result.append(self.delete_image(wiki, image_list))

        return all(result)

    def delete_category(self, wiki, category_list, delete_image=False):
        if not self._check_login_status(wiki):
            self.__log.critical('delete_category: wiki not logged in.')
            return False

        if not isinstance(category_list, list):
            self.__log.critical('delete_category: {0} not list.'.format(category_list))
            return False

        result = []

        for category_title in category_list:
            category = Category(wiki, title=category_title)
            page_list = category.getAllMembers(titleonly=True)
            category_text = category.getWikiText()

            result.append(self.delete_page(wiki, page_list, delete_image))

            if delete_image:
                image_list = self._parse_image_title(category_text)
                result.append(self.delete_image(wiki, image_list))

            try:
                result.append(category.delete())
                self.__log.debug('delete_category: Category {0} deleted.'.format(category_title))
            except:
                result.append(False)
                self.__log.debug('delete_category: Something went wrong when deleting category {0}.'.format(category_title))

        return all(result)

    def delete_page(self, wiki, page_list, delete_image=False):
        if not self._check_login_status(wiki):
            self.__log.critical('delete_page: wiki not logged in.')
            return False

        if not isinstance(page_list, list):
            self.__log.critical('delete_page: {0} not list.'.format(page_list))
            return False

        result = []

        for page_title in page_list:
            page = Page(wiki, title=page_title)
            if not page.exists:
                result.append(False)
                self.__log.debug('delete_page: Page {0} not exist.'.format(page_title))
                continue

            wiki_text = page.getWikiText()

            if delete_image:
                image_list = self._parse_image_title(wiki_text)
                result.append(self.delete_image(wiki, image_list))

            try:
                result.append(page.delete())
                self.__log.debug('delete_page: Page {0} deleted'.format(page_title))
            except:
                self.__log.debug('delete_page: Something went wrong when deleting Page {0}.'.format(page_title))
                result.append(False)

        return all(result)

    def delete_image(self, wiki, image_list):
        if not self._check_login_status(wiki):
            self.__log.critical('delete_image: wiki not logged in.')
            return False

        if not isinstance(image_list, list):
            self.__log.critical('delete_page: {0} not list.'.format(image_list))
            return False

        result = []

        for image_title in image_list:
            file_obj = File(wiki, title=image_title)

            if not file_obj.exists:
                result.append(False)
                self.__log.debug('delete_image: Image {0} not exist.'.format(image_title))
                continue

            try:
                result.append(file_obj.delete())
                self.__log.debug('delete_image: Image {0} deleted.'.format(image_title))
            except:
                result.append(False)
                self.__log.debug('delete_image: Something went wrong when deleting Image {0}.'.format(image_title))

        return all(result)

    def merge_page(self, page_list):
        # TODO: todo, hahaha
        pass

    def _check_login_status(self, wiki):
        try:
            return wiki.isLoggedIn()
        except:
            return False

    def _parse_image_title(self, wiki_text):
        # TODO: Find out better regular expression to reduce further string operations.
        image_list = []
        first_parse = re.findall('\[Image:(.*)\]', wiki_text)

        for item in first_parse:
            try:
                image_name = item.replace(']', '').split('|')[0].strip()
                image_list.append(image_name)
            except:
                self.__log.debug('_parse_image_title: Failed to extract {0}.'.format(item))
                continue

        return image_list


class PDFMgmt(object):

    def __init__(self):
        pass

    @staticmethod
    def print_pdf(url, title, filename, header_title=''):
        options = pdf_options.copy()
        pdf_options['title'] = title
        # Use the following to change the title in the beginning of article.
        additional = 'document.getElementById("firstHeading").innerText = "{0}";'.format(header_title)
        options['run-script'].append(additional)

        try:
            # If url not existed, pdfkit will raise ContentNotFoundError.
            return pdfkit.from_url(url, filename, options=pdf_options)
        except:
            return None


class Logger(object):

    def __init__(self, log_path):
        self._log_file = os.path.join(log_path)

    def debug(self, log_text):
        f = open(self._log_file, 'a')
        text = 'DEBUG: {0}\n'.format(log_text)
        f.write(text)
        f.close()

    def critical(self, log_text):
        f = open(self._log_file, 'a')
        text = 'CRITICAL: {0}\n'.format(log_text)
        f.write(text)
        f.close()
