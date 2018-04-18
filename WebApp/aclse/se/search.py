from elasticsearch import Elasticsearch, helpers
import re

ELASTIC_INDEX= 'pdf_files_small'
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

    def add_author(self, name):
        self.authors_list.append(name)
        self.authors = ", ".join(self.authors_list)

    def set_title(self, title):
        self.title = title

    def set_url(self, url):
        self.url = url

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
            authors = doc["_source"]["meta"]["author"].split(";")
        except:
            pass
        else:
            for _a in authors:
                _re.add_author(_a)

        try:
            path = doc["_source"]["path"]["real"]
        except:
            pass
        else:
            url = "/".join(path.split("/")[9:])
            _re.set_url(url)

        try:
            _re.set_title(doc["_source"]["meta"]["title"])
        except:
            pass

        #content = doc["_source"]["content"]
        # ab_idx = content.split("\n").index("Abstract")
        # int_idx = content.split("\n").index("Introduction")
        abstract = "Sample Text"
        _re.set_summary(abstract)
        result_entries.append(_re)


    qn_message = "Showing {0} of {1} matches returned".format(show_hits, hits)
    context = {'querynum' : qn_message, 'result_entries' : result_entries}
    return context
