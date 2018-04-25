# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crawler.settings import DOC_HOME
from scrapy.http import Request

PDF_HOME = os.path.join(DOC_HOME, "scrapy_data_pdf")
XML_HOME = os.path.join(DOC_HOME, "scrapy_data_xml")

if not os.path.exists(PDF_HOME):
    os.makedirs(PDF_HOME)

if not os.path.exists(XML_HOME):
    os.makedirs(XML_HOME)

METADATA_ROOT = "https://aclanthology.coli.uni-saarland.de/papers/"

class AclwebcrawlSpider(CrawlSpider):
    name = 'aclwebcrawl'
    allowed_domains = ['aclweb.org','aclanthology.coli.uni-saarland.de']
    start_urls = ["http://www.aclweb.org/anthology" ]
    rules = (
        Rule(LinkExtractor(allow=('.pdf',)), callback='parse_pdf', follow=True),
        Rule(LinkExtractor(allow=('^.',)), callback='parse_item', follow=True),
    )

    def parse_item(self,response):
        #print(response.url)
        pass

    def parse_pdf(self,response):
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
        with open(path, 'w+') as f:
            f.write(response.body)

    # def parse(self, response):
    #     sel = Selector(response)
    #     root = response.url
    #     urls = sel.xpath('//a/@href').extract()

        # #_urls = []
        # for url in urls:
        #     if url[:4] != "http":
        #         url = root + url
        #
        #     if url[-3:] == "pdf":
        #         print(url)
        #     else:
        #         AclwebcrawlSpider.url_queue.put(url)
        #
        # #print(list(AclwebcrawlSpider.url_queue.queue))
        # if not AclwebcrawlSpider.url_queue.empty():
        #     print("yield")
        #     yield scrapy.Request(
        #         AclwebcrawlSpider.url_queue.get(),
        #         callback=self.parse
        #     )
