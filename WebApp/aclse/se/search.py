from elasticsearch import Elasticsearch, helpers
import re

ELASTIC_INDEX= 'anthology'
size = 20
ABSTRACT_SIZE = 500
#open connection to Elastic
es = Elasticsearch("localhost:9200")

class ResultsEntry(object):
    def __init__(self):
        self.authors_list = []
        self.authors = ""
        self.url = ""
        self.summary = ""
        self.title = ""
        self.xml = ""
        self.bib = ""

    def add_author(self, name):
        self.authors_list.append(name)
        self.authors = ", ".join(self.authors_list)

    def set_title(self, title):
        self.title = title

    def set_url(self, url):
        self.url = url

    def set_xml(self, xml):
        self.xml = xml

    def set_bib(self, bib):
        self.bib = bib

    def set_summary(self, summary):
        self.summary = summary

def get_search_results(query):
    body = {
                "from": 0,
                "size": size,
                "query": {
                    "query_string": {
                    "query": query
                    }
                }
            }

    res = es.search(index=ELASTIC_INDEX, body= body)
    hit_dict = res.get('hits')
    if hit_dict:
        hits = hit_dict["total"]
    else:
        hits = 0

    if hits >= size:
        show_hits = size
    else:
        show_hits = hits

    result_entries = []
    for doc in hit_dict["hits"]:
        _re = ResultsEntry()
        try:
            authors = doc["_source"]["attachment"]["author"]
        except:
            pass
        else:
            for _a in authors.split(";"):
                _re.add_author(_a)

        # try:
        #     path = doc["_source"]["path"]["real"]
        # except:
        #     pass
        # else:
        #     url = "/".join(path.split("/")[10:])
        #     _re.set_url(url)

        try:
            pdf_url = "/".join(doc["_source"]["pdf_url"].split("/")[-6:])
        except:
            pass
        else:
            _re.set_url(pdf_url)
        # try:
        #     _re.set_url(doc["_source"]["pdf_url"])
        # except:
        #     pass

        try:
            _re.set_url(doc["_source"]["xml_url"])
        except:
            pass

        try:
            _re.set_url(doc["_source"]["bib_url"])
        except:
            pass


        try:
            _re.set_title(doc["_source"]["attachment"]["title"])
        except:
            pass

        try:
            abstract = doc["_source"]["attachment"]["content"][:400]
        except:
            pass
        else:
            _re.set_summary(abstract)

        result_entries.append(_re)


    qn_message = "Showing {0} of {1} matches returned".format(show_hits, hits)
    context = {'querynum' : qn_message, 'result_entries' : result_entries}
    return context
