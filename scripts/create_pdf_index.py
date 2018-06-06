import json
import os
from glob import glob
import base64
import requests
from elasticsearch import Elasticsearch
from elasticsearch.client import IngestClient
from elasticsearch.helpers import parallel_bulk

res = requests.get('http://localhost:9200')
# print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
ingest_client = IngestClient(es)

ingest_body = {
  "description" : "Extract attachment information",
  "processors" : [
    {
      "attachment" : {
        "field" : "data",
        "indexed_chars": "-1",
      },
      "remove": {
        "field": "data"
      }
    }
  ]
}

ingest_client.put_pipeline(id = 1, body = ingest_body)
pipeline = ingest_client.get_pipeline(id = '1')
print("Pipeline : ", pipeline)
doc_home = '/mnt/c/Users/neisa/Documents/Data/Projects/IR/ACLSE/WebApp/documents/'
pdf_path = os.path.join(doc_home,'nlp-data')
# doc_home = '/mnt/c/Users/neisa/Documents/Data/Projects/IR/ACLSE/WebApp/documents/'
# pdf_path = os.path.join(doc_home,'scrapy_data_pdf')
# xml_path = os.path.join(doc_home, 'scrapy_data_xml')
# bib_path = os.path.join(doc_home, 'scrapy_data_bib')

r = requests.get('http://localhost:9200')

print(pdf_path)
#
# def documents():
p_id = 1
i = 0
for root, subfolders, files in os.walk(pdf_path):
    #print(root)
    #print(subfolders)
    #print(files)
    for f in files:
        _fpath = os.path.join(root, f)
        print(_fpath)
        _id = p_id
        p_id += 1
        # if p_id > 10777:
        #     exit()
        with open(_fpath, 'rb') as of:
            data = base64.b64encode(of.read()).decode('ISO-8859-1')
        try:
            body = {
                "data":data,
                "pdf_url":_fpath,
                #"xml_url": os.path.join(xml_path, f.split(".")[0] + ".xml"),
                #"bib_url": os.path.join(bib_path, f.split(".")[0] + ".bib")
            }
            r = es.index(index='anthology', doc_type='pdf', id=p_id, pipeline = '1', body=body)
        except:
            pass
        print(p_id, r, _fpath)
            # json_data = {
            #     '_op_type': 'index',
            #     '_id': p_id,
            #     '_source': {
            #         "body": {"data":data}
            #     }
            # }
            # #print(p_id)
            # yield data
        #     if p_id > 100:
        #         break
        # if p_id > 100:
        #     break

# status = parallel_bulk( es,
#                         documents(),
#                         thread_count=8,
#                         chunk_size=1000,
#                         index="papers_pdf",
#                         doc_type="pdf",
#                         params={"pipeline": "1"})
#
# for ok, result in status:
#     action, res = result.popitem()
#     if not ok:
#         print("failed to index document")
#     else:
#         print("Success!")

out = es.search(index='anthology', doc_type='pdf', q='the', _source_exclude=['data'])
print(out)

#print(list(status))

#i += 1
#print(i)
#if i >=10:
#    exit()
# for idx, file_name in zi
