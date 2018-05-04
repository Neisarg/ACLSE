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
    allowed_domains = ['www.aclweb.org','aclweb.org','aclanthology.coli.uni-saarland.de']
    start_urls = ["https://aclanthology.coli.uni-saarland.de/" ]
    rules = (
        Rule(
            LinkExtractor(
                allow=( '.*\.pdf',),
            ),
            callback = 'parse_pdf',
            follow = True
        ),
        Rule(
            LinkExtractor(
                allow=( '.*\.bib',),
            ),
            callback = 'parse_bib',
            follow = True
        ),
         Rule(
            LinkExtractor(
                allow=( '.*\.xml',),
            ),
            callback = 'parse_xml',
            follow = True
        ),
        Rule(
            LinkExtractor(
                allow=('.*',),
            ),
            callback= 'parse_item',
            follow = True
        )

        #Rule(
        #    LinkExtractor(
        #        allow=( '.*\/[A-Za-z]{1}\/[A-Za-z]{1}[0-9]{2}|$',),
        #    ),
        #    callback = 'parse_item',
        #    follow = True
        #),
        # Rule(LinkExtractor(allow=('.bib',)), callback='parse_bib', follow=True),
        # Rule(LinkExtractor(allow=('.*\/[A-Za-z]{1}\/[A-Za-z]{1}[0-9]{2}|$',)), callback='parse_item', follow=True),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/adminwiki/.*',))),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/portal/.*',))),
        # Rule(LinkExtractor(deny=(r'https://www.aclweb.org/w/.*',))),
    )

    def parse_item(self,response):
        #print(response.url)
        #paths = response.xpath('//a/@href').extract()
        #for path in paths:
        #    url= response.url + path
        #    if path.split('.')[-1] == "pdf":
        #        #print(url)
        #        yield Request(url, callback=self.parse_pdf)
        #    elif path.split('.')[-1] == "bib":
        #        yield Request(url, callback=self.parse_bib)
        url = response.url + ".pdf"
        yield Request(url, callback=self.parse_pdf)
        pass

    def parse_bib(self,response):
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(BIB_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)
        url = response.url[:-3] + "pdf"
        yield Request(url, callback=self.parse_pdf)

    def parse_pdf(self, response):
        if response.status != 200:
            yield
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(PDF_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)
        name = response.url.split('/')[-1].split('.')[0]
        _name = name[0].lower() + name[1:]
        xml_url = METADATA_ROOT + name + "/" + _name + ".xml"
        yield Request(xml_url, callback=self.parse_xml)

    def parse_xml(self,response):
        print(response.url)
        path = response.url.split('/')[-1]
        path = os.path.join(XML_HOME, path)
        with open(path, 'wb') as f:
            f.write(response.body)
