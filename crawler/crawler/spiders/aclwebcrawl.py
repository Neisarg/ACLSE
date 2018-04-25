# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.settings import DOC_HOME
from scrapy.http import Request

PDF_HOME = os.path.join(DOC_HOME, "scrapy_data_pdf")
XML_HOME = os.path.join(DOC_HOME, "scrapy_data_xml")
BIB_HOME = os.path.join(DOC_HOME, "scrapy_data_bib")

if not os.path.exists(PDF_HOME):
    os.makedirs(PDF_HOME)

if not os.path.exists(XML_HOME):
    os.makedirs(XML_HOME)

if not os.path.exists(BIB_HOME):
    os.makedirs(BIB_HOME)

METADATA_ROOT = "https://aclanthology.coli.uni-saarland.de/papers/"

class AclwebcrawlSpider(CrawlSpider):
    name = 'aclwebcrawl'
    allowed_domains = ['www.aclweb.org','www.aclanthology.coli.uni-saarland.de']
    start_urls = ["http://www.aclweb.org/anthology" ]
    rules = (
        Rule(
            LinkExtractor(
                allow=( '.pdf',
                        '.bib',
                        '.*\/[A-Za-z]{1}\/[A-Za-z]{1}[0-9]{2}|$',
                ),
                deny = ( 'http://www.aclweb.org/portal/*',
                         'http://www.aclweb.org/adminwiki/*',
                        'http://www.aclweb.org/anthology/w/*',
                       )
            ),
            callback = 'parse_item',
            follow = True
        ),
        # Rule(LinkExtractor(allow=('.bib',)), callback='parse_bib', follow=True),
        # Rule(LinkExtractor(allow=('.*\/[A-Za-z]{1}\/[A-Za-z]{1}[0-9]{2}|$',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/adminwiki/.*',))),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/portal/.*',))),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/w/.*',))),
    )

    def parse_item(self,response):
        print(response.url)
        path = response.url.split('/')[-1]
        try:
            ftype=path.split('.')[-1]
        except:
            return
        if ftype == "pdf":
            yield Request(response.url, callback=self.parse_pdf)
        elif ftype == "bib":
            yield Request(response.url, callback=self.parse_bib)

    def parse_bib(self,response):
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(BIB_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)

    def parse_pdf(self, response):
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(PDF_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)

        name = path.split('.')[0]
        _name = name[0].lower() + name[1:]
        xml_url = METADATA_ROOT + name + "/" + _name + ".xml"
        yield Request(xml_url, callback=self.parse_xml)

    def parse_xml(self,response):
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(XML_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)
