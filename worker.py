# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import argparse
import tempfile
import concurrent.futures
from urlparse import urlparse

import requests
from lxml import etree
from ebooklib import epub
from slugify import slugify
from unidecode import unidecode
from readability.readability import Document


class Article:

    def __init__(self, url):
        print('Saving page: {}'.format(url))
        res = requests.get(url)
        self.url = url
        self.article = Document(res.content)
        self._add_title()
        self._save_images()

    def _add_title(self):
        self.root = etree.fromstring(self.article.summary())
        body = self.root.find('body')

        title = self.article.title()
        ascii_title = unidecode(title) if type(title) == unicode else title

        title_header = etree.HTML('<h2>{}</h2>'.format(ascii_title))
        body.insert(0, title_header)

    def _save_images(self):
        tmppath = tempfile.mkdtemp()
        images = self.root.xpath('//img')
        for img in images:
            imgsrc = img.get('src')

            # handle scheme-agnostic URLs
            if 'http' not in imgsrc and '//' in imgsrc:
                imgsrc = 'http:{}'.format(imgsrc)

            # handle relative file paths
            elif 'http' not in imgsrc:
                parsed = urlparse(self.url)
                imgsrc = '{}://{}{}'.format(parsed.scheme, parsed.netloc, imgsrc)

            filename = os.path.basename(imgsrc)
            dest = os.path.join(tmppath, filename)

            try:
                res = requests.get(imgsrc)
            except Exception as e:
                print('Could not fetch image ({}) from "{}"'.format(str(e), imgsrc))
                return

            if res.status_code == 404:
                print('Could not fetch image (HTTP 404), attempted fetch: "{}", source URL: {}'.format(imgsrc, img.get('src')))
                continue

            with open(dest, 'wb') as f:
                f.write(res.content)

            img.set('src', dest)

    @property
    def title(self):
        return self.article.title()

    @property
    def html(self):
        return etree.tostring(self.root)


class Book:

    def __init__(self, articles, title, lang='en', id='test-id'):
        self.articles = articles
        self.lang = lang
        self.title = title

        self.book = epub.EpubBook()
        self.book.set_identifier(id)
        self.book.set_title(title)
        self.book.set_language(lang)
        self.book.add_author('Epubify')

        self._add_chapters()

    def _add_chapters(self):
        self.chapters = []
        chapter_no = 1

        for article in self.articles:
            chapter = epub.EpubHtml(title=article.title, file_name='chapter{}.html'.format(chapter_no), lang=self.lang)
            chapter.content = article.html

            self.chapters.append(chapter)
            self.book.add_item(chapter)
            chapter_no += 1

    def write_epub(self, filename=None):
        if filename is None:
            filename = slugify(self.title) + '.epub'

        self.book.toc = (tuple(self.chapters))

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        self.book.spine = ['nav']
        for chapter in self.chapters:
            self.book.spine.append(chapter)

        epub.write_epub(filename, self.book, {})


def create_book(urls, title='Epubify Test Book', filename=None):
    articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(Article, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
                article = future.result()
                articles.append(article)

    book = Book(articles, title)
    print('Writing book to {}'.format(filename))
    book.write_epub(filename)
    return filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--title', required=True, type=str)
    parser.add_argument('-f', '--filename', required=True, type=str)
    parser.add_argument('-u', '--urls', required=True, nargs='+', type=str)
    args = parser.parse_args()

    fname = create_book(args.urls, args.title, args.filename)
